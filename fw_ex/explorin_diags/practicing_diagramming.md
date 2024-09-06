# Planning for Rust Videos

> **Objective of Video**
> 
> Provide the steps to master writing rust code for developing WASM application that can load Neural Network model in Web Browser 

#### Possible Playlist Titles:

> + Mastering Rust and WebAssembly for AI in Web Browsers
> 
> + From Rust to WASM: Deploying AI Models in Web Browsers

Need to have a topic that is attractive and attracts developers to look at the videos

#### Possible 15 Video titles:

```plantuml
skin rose

title Mastrering Rust & WebAssembly for AI in Web Browsers

start 
:Showcase Rust & Wasm in Action;
note left: Load a tokenizer and show the tokenized output
note left: Load a 300MB model and show how the browser performs

:Introducing Rust;
note right:Dive into the important concepts of Rust
```

```plantuml
skin rose

title Mastrering Rust & WebAssembly for AI in Web Browsers


Class "ShowcaseRust&Wasm_in_Action"{
    Load a tokenizer and show the tokenized output
    Load a 300MB model and show how the browser performs
}
Class IntroducingRust{
    Dive into the important concepts of Rust
}
Enum Chooser {
    Right
    Left
}
IntroducingRust --> Chooser
Interface WASM {
    Minutes
}
class BucketList{
    + Make Pizza
    - Try skiing
}
BucketList -> WASM 
WASM --> Chooser


Class Outer {
    step one
    step two
}

Class three{
    Makes Sense
}

Class nextOuter{
    step1
    step2
}

nextOuter::step1 --> Outer : "has a"
nextOuter::step2 --> three : "goes to"
```

```flowchart
st =>start: Mastering Rust & WebAssembly for AI in Web Browsers
op1 =>operation: Showcase Rust & Wasm in Action
pa2 => parallel: Load a tokenizer and show the tokenized output
pa3 =>parallel: Load a 300MB model and show how the browser performs
io =>inputoutput: Introducing Rust
p1 =>parallel: Dive into Rust DataTypes
p2 =>parallel: Learn about 
p3 =>parallel: Dive into Rust variable
p4 =>parallel: Dive into Rust variable

st -> op1
op1 -> pa2
op1 -> pa3
```

```flowchart
st=>start: Start|past
op1=>operation: Step 1 Initialize|past
op2=>operation: Parallel Task A|past
op3=>operation: Parallel Task B|past
c1=>condition: Continue Process?
end=>end: End

st->op1
op1->c1
c1(yes)->op2
c1(no)->end
op2->op3
```

```plantuml
@startmindmap
* Mastrering Rust & WebAssembly for AI in Web Browsers
** Showcase: "Rust & Wasm in Action"
*** noteleft: "Load a tokenizer and show the tokenized output"
*** noteleft: "Load a 300MB model and show how the browser performs"
** IntroducingRust
*** noteright: "Dive into the important concepts of Rust"
@endmindmap
```

```plantuml
@startmindmap
* Your Experience with Rust
** Very new to Rust
*** Options
*** Unwrap explained
*** Result Type
**** Parsing Integer
**** Result Alias
** Got some functional language experience
** Comfortable and already well rusted
@endmindmap
```

```mermaid
classDiagram
    OuterClass --> InnerClass : contains
    class OuterClass {
      +String outerAttribute1
      +int outerAttribute2
    }
    class InnerClass {
      +String innerAttribute1
      +int innerAttribute2
    }
    class InnerClass1 {
      +String innerAttribute1
      +int innerAttribute2
    }
    class InnerClass2 {
      +String innerAttribute1
      +int innerAttribute2
    }
```

```mermaid
graph TD
    K[Open Topic]
    L[Open Topic 2]
    K --> L
    A[Central Idea] --> B[Main Topic 1]
    A --> C[Main Topic 2]
    A --> D[Main Topic 3]
    B --> E[Subtopic 1.1]
    B --> F[Subtopic 1.2]
    C --> G[Subtopic 2.1]
    D --> H[Subtopic 3.1]
    D --> I[Subtopic 3.2]
    D --> J[Subtopic 3.3]
    J --> K
```

```mermaid
graph RL
    A[Top]
    B[Next]
    A --> B
```

```flowchart
st=>start: Begin
op1=>operation: task1
e=>end: end
st->op1
op1->e
```

##### Practice:1

- Class Diagram

```mermaid
classDiagram
    class One {
        +step1
        +step2
    }
    class Two {
        +step3
    }
    One --> Two 
```

```plantuml
Class One {
    Step 1
    Step 2
}

Class Two {
    Step2
    Step 3
}
Two::Step2 --> One

Class Three {
    task1: Step 2 become detached
    task2: Step3
}
Three::task2 --> One
Three::task1 --> Two
```

```mermaid
graph RL
    A[step 1]
    B[step 2]
    A --> B
```

```plantuml
@startuml
   Class One {
    t1: Task 1
    t2: Task 2
    }

    Class Two {
        Task 3
        Task 4
    }
    Enum Nums {
        One
        Two
        Three
    }
    Struct s1 {
        s:Name
        i:age
    }
    One::t1 --> Two : Contains
    s1::s --> Nums::One : Connects
@enduml
```

```mermaid
graph RL
    A[one]
    B[two]
    A --> B
    K[Three]
    A --> K
    F[Theory]
    F --> B
```

```flowchart
st=>start: what is your knowlege leel?| past
state=>condition: Decide one
new=>operation: New to Rust|current
experienced=>operation: Have experience in functional lang|current
rusty=>operation: Good experienced and 'rusted' well|past

st->state
state(yes)->new
state(no)->experienced
state(yes)->rusty
```

```mermaid
graph TD
    h0[Your experience with rust]
    t01[New to rust]
    t02[Got functional Code experience]
    t03[Well rusted experience]
    h0 --> t01
    h0 --> t02
    h0 --> t03
```

```plantuml
@startmindmap

* HR Systems Mapping
** Workday
*** <b>name</b></back>
*** <b>firstname</b></back>
*** <b>education</b></back>
*** <b>designation</b></back>
** ADP
*** <b>lastname</b></back> : <back:lightblue><b>'name'</b></back>
*** <b>firstname</b></back> : <back:lightgreen><b>'firstname'</b></back>
*** <b>education</b></back> : <back:lightgreen><b>'education'</b></back>
*** <b>position</b></back> : <back:lightblue><b>'designation'</b></back>
** Greenhouse
*** <b>name</b></back> : <back:lightgreen><b>'name'</b></back>
*** <b>firstname</b></back> : <back:lightgreen><b>'firstname'</b></back>
*** <b>education</b></back> : <back:lightgreen><b>'education'</b></back>
*** <b>designation</b></back> : <back:lightgreen><b>'designation'</b></back>

@endmindmap
```

```plantuml
@startmindmap
* Greenhouse(Source of Truth)
** Candidate ID
*** Applicant_ID -> Workday
*** n/a (not applicable) -> ADP
** First Name
*** Legal First Name -> Workday
*** First Name -> ADP
** Preferred name (First & Last name)
*** Preferred Name -> Workday
*** Preferred First & Last Name -> ADP
** Legal Last Name
*** Legal Last Name -> Workday
*** Last Name -> ADP
** Personal Email
*** Home Email Address -> Workday
*** Personal E-mail -> ADP
** Starts At
*** offer Start date -> Workday
*** Hire date -> ADP
** Contractor/Intern End Date
*** End date -> Workday
*** Termination Date -> ADP
@endmindmap
```

```mermaid
flowchart LR
    A[Start]:::red --> B{Is it a weekday?}
    B -->|Yes| C[Work]:::orange
    B -->|No| D[Relax]:::red
    C --> E[Continue Working]
    D --> E[Enjoy]:::yellow
    E --> F[End]:::green

    classDef red fill:#ffcccc;
    classDef orange fill:#ffdd99;
    classDef green fill:#d3f261;
    classDef yellow fill:#ffffcc;
    classDef blue fill:#d0e7ff;
```

```flowchart
st=>start: Square 1
op=>operation: Square 2
op2=>operation: Square 3
op3=>operation: Square 4
op4=>operation: Square 5

st->op(right)->op2->op3(right)->op4
```

```flowchart
```flowchart
st=>start: Start|past:>[style.fill=#ffccff]
op1=>operation: Operation 1|past:>[style.fill=#ffdd99]
op2=>operation: Operation 2|current:>[style.fill=#ffffcc]
cond=>condition: Condition?|approved:>[style.fill=#d3f261]
e=>end: End|future:>[style.fill=#d0e7ff]

st(right)->op1(right)->cond
cond(yes,right)->op2(right)->e
cond(no,bottom)->e
```

```mermaid
flowchart LR
    A[Start]:::red --> B[Operation 1]:::orange
    B --> C{Condition?}:::green
    C -->|Yes| D[Operation 2]:::yellow
    C -->|No| E[End]:::blue

    classDef red fill:#ffcccc;
    classDef orange fill:#ffdd99;
    classDef green fill:#d3f261;
    classDef yellow fill:#ffffcc;
    classDef blue fill:#d0e7ff;
```

```vega-lite
{
  "data": {
    "values": [
      {"a": "C", "b": 2}, {"a": "C", "b": 7}, {"a": "C", "b": 4},
      {"a": "D", "b": 1}, {"a": "D", "b": 2}, {"a": "D", "b": 6},
      {"a": "E", "b": 8}, {"a": "E", "b": 4}, {"a": "E", "b": 7}
    ]
  },
  "mark": "point",
  "encoding": {
    "x": {"field": "a", "type": "nominal"},
    "y": {"field": "b", "type": "quantitative"}
  }
}
```
