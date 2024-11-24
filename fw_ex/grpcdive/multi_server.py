#!/bin/python

import grpc
from concurrent import futures
import multi_service_pb2 as pb2
import multi_service_pb2_grpc as pb2_grpc
from person import Person
from sqlmodel import select, create_engine, Session

engine = create_engine("sqlite:///person.db", connect_args={"check_same_thread": False})
session = Session(engine)


class PersonService(pb2_grpc.PersonServiceServicer):
    def GetPersonById(self, request, context):
        get_id = request.id
        person = session.get(Person, get_id)
        return pb2.PersonResponse(
            name=person.name, age=person.age, location=person.location, id=person.id
        )

    def DeletePersonById(self, request, context):
        get_id = request.id
        person = session.get(Person, get_id)
        if not person:
            return pb2.DeletePersonById(status="Person Missing")
        session.delete(person)
        session.commit()
        return pb2.DeletePersonResponse(status="Person Deleted")

    def CreatePerson(self, request, context):
        person = Person(name=request.name, age=request.age, location=request.location)
        session.add(person)
        session.commit()
        session.refresh(person)
        message = f"Person is: {person.name} and staying at {person.location}"
        return pb2.CreatePersonResponse(id=person.id, message=message)

    def ListPersons(self, request, context):
        persons = session.exec(select(Person)).all()
        for person in persons:
            yield pb2.PersonResponse(
                name=person.name, age=person.age, location=person.location, id=person.id
            )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    pb2_grpc.add_PersonServiceServicer_to_server(PersonService(), server)
    server.add_insecure_port("[::]:5055")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
