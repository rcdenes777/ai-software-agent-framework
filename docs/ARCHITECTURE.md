# AI Software Agent Framework — Architecture

## Visão Geral

Este repositório define uma arquitetura reutilizável para agentes de inteligência artificial voltados ao desenvolvimento de software.

O objetivo é separar responsabilidades entre agentes especializados.

---

# Arquitetura de Agentes

Fluxo principal:

Usuário

↓

Project Manager

↓

Executor

↓

Test Engineering

↓

Revisão e atualização do projeto

---

# Papéis

## Project Manager

Responsável por:

- entender a visão do usuário;
- planejar o projeto;
- definir requisitos;
- controlar escopo;
- criar roadmap;
- dividir fases;
- criar tarefas;
- revisar entregas.

Não é responsável por implementar código diretamente.

---

## Executor

Responsável por:

- executar tarefas técnicas;
- modificar código;
- criar testes;
- validar implementação;
- reportar resultados.

Recebe tarefas previamente estruturadas.

---

## Test Engineering

Responsável por:

- avaliar estratégia de testes;
- revisar cobertura;
- analisar riscos;
- sugerir melhorias de validação.

---

# Skills

## project-manager-core

Define o comportamento do Gerente Técnico.

## task-complexity-analyzer

Classifica a complexidade das tarefas.

Níveis:

- Lua
- Terra
- Sol

## test-engineering-core

Define práticas de validação e qualidade.

---

# Princípios

## Separação de responsabilidades

Cada agente possui uma função clara.

## Rastreabilidade

Decisões, fases e alterações devem ser registradas.

## Controle de escopo

O projeto deve evoluir de forma planejada.

## Qualidade

Nenhuma entrega é considerada concluída sem validação adequada.

---

# Objetivo Final

Criar uma arquitetura de agentes capaz de conduzir projetos de software desde a ideia inicial até a entrega, mantendo planejamento, execução e qualidade organizados.
