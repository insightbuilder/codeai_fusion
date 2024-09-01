```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE-ITEM : contains
    PRODUCT ||--o{ LINE-ITEM : identified_by
    CUSTOMER {
        int customerID
        string name
        string email
    }
    ORDER {
        int orderID
        date orderDate
    }
    LINE-ITEM {
        int lineItemID
        int quantity
    }
    PRODUCT {
        int productID
        string name
        float price
    }
```

Trying to figure out a way to represent below into a mapping

| Workday     | ADP       | Greenhouse  |
| ----------- | --------- | ----------- |
| name        | lastname  | name        |
| firstname   | firstname | firstname   |
| education   | education | education   |
| designation | position  | designation |

```plantuml
@startuml

entity Workday {
    * name
    * firstname
    * education
    * designation
}

entity ADP {
    * lastname
    * firstname
    * education
    * position
}

entity Greenhouse {
    * name
    * firstname
    * education
    * designation
}

Workday::name -- ADP::lastname : maps to
Workday::firstname -- ADP::firstname : identical
Workday::education -- ADP::education : identical
Workday::designation -- ADP::position : maps to

Workday::name -- Greenhouse::name : identical
Workday::firstname -- Greenhouse::firstname : identical
Workday::education -- Greenhouse::education : identical
Workday::designation -- Greenhouse::designation : identical

@enduml
```

```plantuml
@startuml

package "HR Systems Mapping" {
    entity Workday {
        * name
        * firstname
        * education
        * designation
    }

    entity ADP {
        * lastname
        * firstname
        * education
        * position
    }

    entity Greenhouse {
        * name
        * firstname
        * education
        * designation
    }
}

' Associations between Workday and ADP
Workday::name -- ADP::lastname : "maps to"
Workday::firstname -- ADP::firstname : "identical"
Workday::education -- ADP::education : "identical"
Workday::designation -- ADP::position : "maps to"

' Associations between Workday and Greenhouse
Workday::name -- Greenhouse::name : "identical"
Workday::firstname -- Greenhouse::firstname : "identical"
Workday::education -- Greenhouse::education : "identical"
Workday::designation -- Greenhouse::designation : "identical"

@enduml
```

```plantuml
@startuml

package Workday {
    object name {
        fieldName = "name"
        entity = "Workday"
    }

    object firstname {
        fieldName = "firstname"
        entity = "Workday"
    }

    object education {
        fieldName = "education"
        entity = "Workday"
    }

    object designation {
        fieldName = "designation"
        entity = "Workday"
    }
}

package ADP {
    object lastname {
        fieldName = "lastname"
        entity = "ADP"
    }

    object firstname_ADP {
        fieldName = "firstname"
        entity = "ADP"
    }

    object education_AD {
        fieldName = "education"
        entity = "ADP"
    }

    object position {
        fieldName = "position"
        entity = "ADP"
    }
}

package Greenhouse {
    object name_GH {
        fieldName = "name"
        entity = "Greenhouse"
    }

    object firstname_GH {
        fieldName = "firstname"
        entity = "Greenhouse"
    }

    object education_GH {
        fieldName = "education"
        entity = "Greenhouse"
    }

    object designation_GH {
        fieldName = "designation"
        entity = "Greenhouse"
    }
}

' Associations between objects to show mapping
name -- lastname : maps to
firstname -- firstname_ADP : identical
education -- education_ADP : identical
designation -- position : maps to

name -- name_GH : identical
firstname -- firstname_GH : identical
education -- education_GH : identical
designation -- designation_GH : identical
@enduml
```

```plantuml
@startmindmap
* HR Systems Mapping
** Workday
*** "name"
*** "firstname"
*** "education"
*** "designation"
** ADP
*** "lastname" : "maps to 'name'"
*** "firstname" : "identical to 'firstname'"
*** "education" : "identical to 'education'"
*** "position" : "maps to 'designation'"
** Greenhouse
*** "name" : "identical to 'name'"
*** "firstname" : "identical to 'firstname'"
*** "education" : "identical to 'education'"
*** "designation" : "identical to 'designation'"
@endmindmap
```

```plantuml
@startmindmap
* HR Systems Mapping
** "Workday"
*** "name"
**** "ADP: lastname" : "maps to 'name'"
**** "Greenhouse: name" : "identical to 'name'"
*** "firstname"
**** "ADP: firstname" : "identical to 'firstname'"
**** "Greenhouse: firstname" : "identical to 'firstname'"
*** "education"
**** "ADP: education" : "identical to 'education'"
**** "Greenhouse: education" : "identical to 'education'"
*** "designation"
**** "ADP: position" : "maps to 'designation'"
**** "Greenhouse: designation" : "identical to 'designation'"
** "ADP"
*** "lastname" 
**** "Workday: name" : "maps to 'lastname'"
**** "Greenhouse: name" : "maps to 'name'"
*** "firstname"
**** "Workday: firstname" : "identical to 'firstname'"
**** "Greenhouse: firstname" : "identical to 'firstname'"
*** "education"
**** "Workday: education" : "identical to 'education'"
**** "Greenhouse: education" : "identical to 'education'"
*** "position"
**** "Workday: designation" : "maps to 'position'"
**** "Greenhouse: designation" : "identical to 'designation'"
** "Greenhouse"
*** "name" 
**** "Workday: name" : "identical to 'name'"
**** "ADP: lastname" : "maps to 'name'"
*** "firstname"
**** "Workday: firstname" : "identical to 'firstname'"
**** "ADP: firstname" : "identical to 'firstname'"
*** "education"
**** "Workday: education" : "identical to 'education'"
**** "ADP: education" : "identical to 'education'"
*** "designation"
**** "Workday: designation" : "identical to 'designation'"
**** "ADP: position" : "maps to 'designation'"
@endmindmap
```

```plantuml
@startmindmap
* HR Systems Mapping
** Workday
*** "name"
*** "firstname"
*** "education"
*** "designation"
** ADP
*** "<back:lightblue>lastname</back>" : "<back:lightgreen>maps to 'name'</back>"
*** "<back:lightgreen>firstname</back>" : "<back:lightgreen>identical to 'firstname'</back>"
*** "<back:lightgreen>education</back>" : "<back:lightgreen>identical to 'education'</back>"
*** "<back:lightblue>position</back>" : "<back:lightgreen>maps to 'designation'</back>"
** Greenhouse
*** "<back:lightgreen>name</back>" : "<back:lightgreen>identical to 'name'</back>"
*** "<back:lightgreen>firstname</back>" : "<back:lightgreen>identical to 'firstname'</back>"
*** "<back:lightgreen>education</back>" : "<back:lightgreen>identical to 'education'</back>"
*** "<back:lightgreen>designation</back>" : "<back:lightgreen>identical to 'designation'</back>"

@endmindmap
```

```plantuml
@startmindmap

* HR Systems Mapping
** Workday
*** <back:cream><b>name</b></back>
*** <back:cream><b>firstname</b></back>
*** <back:cream><b>education</b></back>
*** <back:cream><b>designation</b></back>
** ADP
*** <back:cream><b>lastname</b></back> : <back:lightblue><b>maps to 'name'</b></back>
*** <back:cream><b>firstname</b></back> : <back:lightgreen><b>identical to 'firstname'</b></back>
*** <back:cream><b>education</b></back> : <back:lightgreen><b>identical to 'education'</b></back>
*** <back:cream><b>position</b></back> : <back:lightblue><b>maps to 'designation'</b></back>
** Greenhouse
*** <back:cream><b>name</b></back> : <back:lightgreen><b>identical to 'name'</b></back>
*** <back:cream><b>firstname</b></back> : <back:lightgreen><b>identical to 'firstname'</b></back>
*** <back:cream><b>education</b></back> : <back:lightgreen><b>identical to 'education'</b></back>
*** <back:cream><b>designation</b></back> : <back:lightgreen><b>identical to 'designation'</b></back>

@endmindmap
```
