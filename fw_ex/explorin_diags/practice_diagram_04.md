---
Date 12th Sep

Practice Diagramming Based on Teaching Diagramming
---

##### The Main Diagram options in PlantUML

```plantuml
title Class Diagram of Diagramming
@startuml
class Sequence{
    a: HasParticipants
    b: Provides communication between them
    c: Connected using arrows
    }
class ClassDiag{
    a: Same as OOP class / Json Obj
    b: Has attributes
    }
class mindMap {
    a: map of concepts
    b: ability to provide colors
    c: support like legend
}
@enduml
```

```plantuml
title Sequence Diagram of Making Diagrams
"have thought" -> "Diagram": Choose
"Diagram" -> "Make Diagram": 1st cut
"Make Diagram" -> "Display": Show on
"Display" -> "have thought": Feedback
"have thought" -> "Make Diagram": Update
"Display" -> "have thought": change diagram
```

```plantuml
title Rust Language
@startmindmap
*[#cyan] **Learning Rust**
**[#lightgreen] **Why Learn**
***[#pink] **Make Computer Work For You**
***[#pink] **Designed for Feedback**
***[#pink] **Visualise Memory management**
***[#pink] **Super Fast execution**
***[#pink] **Ecosystem of Tools**
***[#pink] **Robust Dependency Management**
**[#yellow] **How Learn**
***[#orange] **Practice Variables**
***[#orange] **Understand Types**
****[#brown] **Enums**
*****[#green] **Options**
*****[#green] **Results**
****[#brown] **Structs**
***[#orange] **Learn Functions**
***[#orange] **Traits of Functions**
***[#orange] **Dive into Pointers**
****[#lightblue] **Ref Counted**
****[#lightblue] **Box**
****[#lightblue] **Atomic RC**
****[#lightblue] **Clone on Write**
***[#orange] **cargo tool**
***[#orange] **Workspace Mangement**
***[#orange] **Threading**
***[#orange] **Macros**
@endmindmap
```

```plantuml
title Learning Flowchart in PlantUML
@startuml
start
if (Condition) then (Yes)
    :Do something;
else (No)
    :Do something else;
endif
stop
@enduml
```

```flowchart
st=>start: Decided to Learn Rust
op1=>operation: Think why learn Rust
c1=>condition: Found answer
opy=>operation: Figure out How to learn
opn=>operation: Research and make your mind 
c2=>condition: Done
e=>end: Completed Rust Practice-
st->op1
op1->c1(yes)
c1(yes)->opy
c1(no)->opn
opn->c2
c2(no)->opn
c2(yes)->opy
```

```mermaid
classDiagram 
    class one{
        attr1
        attr2
    }
    class two{
        attr1
        attr2
    }
    one --> two
```

```mermaid
graph TD
    a[Decided to learn Rust] --> b[Why Learn]
    a --> c[How learn]
    a --> d[How Practice]
```

@startuml

skin rose

title Simple State Model
[*] --> GlassEmpty
GlassEmpty --> [*]
GlassEmpty : Contents - void

GlassEmpty -> GlassFull
GlassFull : Water
GlassFull --> [*]

note right
this is a note
end note

@enduml

```plantuml
@startuml
title State Diagram
[*] --> Decide_to_Learn_Rust


Decide_to_Learn_Rust: Ideas-Why
Decide_to_Learn_Rust->Learnt_Rust
Learnt_Rust: Ideas-How
Learnt_Rust -->[*]
@enduml
```

@startuml

skin rose

title Simple Composite State Model
[*] --> NeilDiamond
state NeilDiamond 

state "Neil Diamond" as NeilDiamond {
  state Dancing
  state Singing
  state Smiling
  Dancing --> Singing
  Singing --> Smiling
  Smiling --> Dancing
}

@enduml
