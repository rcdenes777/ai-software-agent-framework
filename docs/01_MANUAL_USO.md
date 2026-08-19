# Manual de Uso --- AI Software Agent Framework

## Objetivo

Este documento descreve como utilizar o framework de agentes Hermes para
conduzir projetos de software utilizando separação de responsabilidades
entre humano, gerente técnico e executores.

O framework tem como objetivo organizar planejamento, execução e
validação de projetos utilizando agentes especializados.

------------------------------------------------------------------------

# Modelo de trabalho

O fluxo principal é:

    HUMANO
       |
       v
    PROJECT MANAGER
    (Gerente Técnico)
       |
       v
    EXECUTOR
       |
       v
    TEST ENGINEERING
       |
       v
    REVISÃO

O humano permanece como responsável pelas decisões finais.

------------------------------------------------------------------------

# Papel do Humano

O humano é responsável por:

-   definir objetivos;
-   aprovar mudanças importantes;
-   decidir prioridades;
-   validar decisões de arquitetura;
-   autorizar alterações sensíveis.

O agente auxilia na execução, mas não substitui a decisão humana.

------------------------------------------------------------------------

# Papel do Project Manager

O Project Manager atua como Gerente Técnico.

Responsabilidades:

-   compreender a visão do projeto;
-   analisar requisitos;
-   definir escopo;
-   criar roadmap;
-   dividir fases;
-   criar tarefas;
-   classificar complexidade;
-   revisar entregas.

O Gerente não deve implementar diretamente tarefas de código quando
existe um Executor disponível.

------------------------------------------------------------------------

# Papel do Executor

O Executor recebe tarefas estruturadas pelo Gerente.

Responsabilidades:

-   implementar código;
-   criar testes;
-   executar validações;
-   modificar arquivos autorizados;
-   retornar resultados.

O Executor não deve:

-   alterar arquitetura por conta própria;
-   expandir escopo;
-   tomar decisões de produto;
-   substituir o planejamento do Gerente.

------------------------------------------------------------------------

# Processo recomendado

## 1. Solicitação

O humano apresenta uma ideia ou necessidade.

Exemplo:

"Adicionar sistema de ranking ao StreamRank Lab."

------------------------------------------------------------------------

## 2. Análise

O Gerente avalia:

-   objetivo;
-   impacto;
-   riscos;
-   arquivos envolvidos;
-   complexidade.

------------------------------------------------------------------------

## 3. Planejamento

O Gerente cria:

-   plano;
-   tarefas menores;
-   critérios de aceite;
-   testes necessários.

------------------------------------------------------------------------

## 4. Aprovação

Decisões de produto e arquitetura aguardam aprovação humana quando
necessário.

------------------------------------------------------------------------

## 5. Execução

O Executor recebe uma tarefa clara e limitada.

------------------------------------------------------------------------

## 6. Revisão

O Gerente verifica:

-   código alterado;
-   testes;
-   conformidade;
-   riscos;
-   próximos passos.

------------------------------------------------------------------------

# Regra de distribuição de tarefas

Modelo recomendado:

    Gerente
     |
     +-- Executor Pro
     |      |
     |      +-- arquitetura complexa
     |      +-- grandes refatorações
     |      +-- problemas difíceis
     |
     +-- Executor Flash
            |
            +-- tarefas simples
            +-- ajustes isolados
            +-- documentação
            +-- testes básicos

------------------------------------------------------------------------

# Princípios

## Separação de responsabilidades

Cada agente possui uma função definida.

## Rastreabilidade

Decisões, tarefas e resultados devem ser registrados.

## Controle de escopo

O projeto deve evoluir de forma planejada.

## Qualidade

Nenhuma entrega é considerada concluída sem validação.

------------------------------------------------------------------------

# Objetivo final

Criar um ambiente onde:

-   o humano decide;
-   o gerente coordena;
-   o executor implementa;
-   a qualidade é validada.

A separação permite projetos maiores com mais controle e
previsibilidade.
