# ADR-Eloquent-ORM-choice.md

## Title
Use Eloquent-ORM

## Context
We need to communicate with MySQL for inserting, updating , deleting and searching data.

## Decision
We chose Eloquent ORM to make database interactions both powerfull and elegant.

## Rationale
- Expressive, Readable Syntax
- Model-Centric Structure(each table has a model inside application with its own parents and children)
- Effortless Relationship Management

## Alternatives considered:
- Raw SQL(Lightweight Mapping but more boilerplate and manual mapping)
- Data Access Objects (DAO):Separation of concerns but Potential for repetitive or scattered code if not structured well.

## Consequences
- Accurate queries
- No Confusion


## References
- https://manoj-shu100.medium.com/eloquent-orm-in-laravel-simplifying-database-interactions-b0269942f190