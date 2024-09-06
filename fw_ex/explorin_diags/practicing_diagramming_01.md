---
Date: 3rd Sep
Time: 6:06 AM
Session: 02
---

##### Practice Plan:

Class Diagrams on PlantUML

```plantuml
@startuml
    Class One {
        t1: task1
        t2: task2
    }
    Class Two {
        t1: task1
        t2: task2
    }
    Enum Choices{
        k1:Choice1
        k2:Choice2
    }
    One::t1 -> Two::t1
    Two::t2 -> Choices:k1 | disconnect
    One::t2 -> Choices:k2 | connect
@enduml
```

MindMaps on Plantuml

```plantuml
@startmindmap
* AllTasks
** One
*** task1
**** k1
*** task2
**** k2
** Two
*** task1
**** k2
*** task2
**** k1
@endmindmap
```

Class Diagrams on Mermaid

```mermaid
classDiagram
    class One {
        task1
        task2
    }
    class Two {
        task1
        task2
    }
    One --> Two
```

FlowChart on Mermaid

```mermaid
graph TD
    One --> one-task1
    One --> one-task2
    Two --> two-task1
    Two --> two-task2
    one-task1 --> k1
    one-task2 --> k2
    two-task2 --> k1
    two-task1 --> k2
```

Flowchart on Flowchart JS

```flowchart
mst=>start: StartHere| past
mc=>condition: split here| current
st1=>operation: One|past
c1=>condition: which task|past
ot1=>operation: Task1|current
ot2=>operation: Task2|current
st2=>operation: Two|past
c2=>condition: which task|past
oo1=>operation: Task1|current
oo2=>operation: Task2|current
e=>end: End|past
mst->mc
mc(yes)->st1
st1->c1
c1(yes)->ot1
c1(no)->ot2
mc(no)->st2
st2->c2
c2(yes)->oo1
c2(no)->oo2
```
