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
* Mastrering RusT & WebAssembly for AI in Web Browsers
** Showcase: "Rust & Wasm in Action"
*** noteleft: "Load a tokenizer and show the tokenized output"
*** noteleft: "Load a 300MB model and show how the browser performs"
** IntroducingRust
*** noteright: "Dive into the important concepts of Rust"
@endmindmap
```
