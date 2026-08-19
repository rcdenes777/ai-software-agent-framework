# Arquitetura de Agentes --- AI Software Agent Framework

## Visão Geral

O framework define uma arquitetura de desenvolvimento baseada em agentes
especializados.

O objetivo é separar responsabilidades entre:

-   Humano;
-   Gerente de Projeto;
-   Executor;
-   Engenharia de Testes;
-   Revisão.

A arquitetura evita que um único agente acumule planejamento, decisão e
implementação.

------------------------------------------------------------------------

# Arquitetura Geral

                        HUMANO
                           |
                           v
                  GERENTE DE PROJETO
                  (Hermes Manager)
                           |
            +--------------+--------------+
            |                             |
            v                             v
     EXECUTOR PRO                   EXECUTOR FLASH
     tarefas complexas              tarefas simples/médias
                           |
                           v
                  TESTES E VALIDAÇÃO
                           |
                           v
                        REVISÃO

------------------------------------------------------------------------

# Humano

O humano é a autoridade final.

Responsabilidades:

-   definir objetivos;
-   aprovar decisões importantes;
-   validar arquitetura;
-   definir prioridades;
-   aceitar ou rejeitar entregas.

O agente auxilia na tomada de decisão, mas não substitui o controle
humano.

------------------------------------------------------------------------

# Gerente de Projeto

O Gerente funciona como um Tech Lead.

Responsabilidades:

-   entender a visão do projeto;
-   analisar requisitos;
-   definir estratégia;
-   controlar escopo;
-   criar roadmap;
-   dividir tarefas;
-   classificar complexidade;
-   revisar resultados.

O Gerente decide:

-   qual tarefa será executada;
-   qual executor é adequado;
-   quais critérios de aceite existem;
-   quando uma tarefa está concluída.

------------------------------------------------------------------------

# Executor Pro

Uso recomendado:

-   arquitetura complexa;
-   grandes refatorações;
-   problemas difíceis;
-   migrações;
-   decisões técnicas já aprovadas.

Características:

-   maior capacidade de raciocínio;
-   usado em tarefas de alto impacto;
-   custo maior.

------------------------------------------------------------------------

# Executor Flash

Uso recomendado:

-   tarefas simples;
-   ajustes isolados;
-   documentação;
-   testes;
-   pequenas implementações.

Características:

-   execução rápida;
-   menor custo;
-   adequado para tarefas bem definidas.

------------------------------------------------------------------------

# Regra fundamental

O Executor não decide arquitetura.

O Executor:

-   recebe uma tarefa;
-   implementa;
-   testa;
-   informa resultados.

O Executor não deve:

-   mudar escopo;
-   escolher tecnologias sem autorização;
-   redefinir regras de negócio;
-   substituir o planejamento.

------------------------------------------------------------------------

# Fluxo de Desenvolvimento

    Humano apresenta objetivo

            ↓

    Gerente analisa

            ↓

    Gerente cria plano e tarefas

            ↓

    Humano aprova decisões necessárias

            ↓

    Executor implementa

            ↓

    Gerente revisa

            ↓

    Projeto atualizado

------------------------------------------------------------------------

# Delegate Task x Executor Run

## delegate_task

É uma delegação interna do Hermes.

Características:

-   cria um subagente dentro do contexto atual;
-   normalmente herda o modelo do agente pai;
-   não representa necessariamente outro profile.

Foi identificado que ele não substitui automaticamente o Executor Flash.

------------------------------------------------------------------------

## executor-run

É a ponte utilizada para chamar um profile separado.

Fluxo:

    Hermes Manager
          |
          v
    executor-run
          |
          v
    hermes -p streamrank-executor
          |
          v
    DeepSeek Flash

Esse fluxo mantém a separação real entre gerente e executor.

------------------------------------------------------------------------

# Princípios da Arquitetura

## Separação de responsabilidades

Cada agente possui uma função específica.

## Rastreabilidade

Toda tarefa deve possuir:

-   objetivo;
-   escopo;
-   arquivos envolvidos;
-   testes;
-   resultado.

## Controle de qualidade

O Gerente valida a entrega antes de considerar concluída.

## Escalonamento

Tarefas simples usam Flash.

Tarefas complexas usam Pro.

------------------------------------------------------------------------

# Objetivo Final

Construir uma equipe virtual de desenvolvimento:

Humano: decide.

Gerente: planeja e coordena.

Executor: implementa.

Testes: validam.

Revisão: garante qualidade.
