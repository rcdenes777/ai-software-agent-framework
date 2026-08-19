# Fluxo de Desenvolvimento --- AI Software Agent Framework

## Objetivo

Este documento descreve o fluxo operacional recomendado para
desenvolvimento utilizando a arquitetura de agentes Hermes.

O objetivo é manter separadas as etapas de:

-   definição;
-   planejamento;
-   execução;
-   validação;
-   histórico.

------------------------------------------------------------------------

# Fluxo Completo

    IDEIA DO HUMANO
            |
            v
    ANÁLISE DO GERENTE
            |
            v
    CLASSIFICAÇÃO DA TAREFA
            |
            v
    DECISÃO / APROVAÇÃO HUMANA
            |
            v
    HANDOFF PARA EXECUTOR
            |
            v
    IMPLEMENTAÇÃO
            |
            v
    TESTES
            |
            v
    REVISÃO DO GERENTE
            |
            v
    REGISTRO DO RESULTADO

------------------------------------------------------------------------

# 1. Ideia Inicial

O processo começa quando o humano apresenta um objetivo.

Exemplo:

"Adicionar ranking inteligente ao StreamRank Lab."

Neste momento não existe implementação.

O objetivo é apenas informar a necessidade.

------------------------------------------------------------------------

# 2. Análise do Gerente

O Gerente avalia:

-   objetivo;
-   impacto;
-   dependências;
-   riscos;
-   arquivos envolvidos;
-   possíveis soluções.

O Gerente não executa código nesta etapa.

------------------------------------------------------------------------

# 3. Classificação da Tarefa

A tarefa recebe uma classificação de complexidade.

Exemplo:

-   Baixa;
-   Média;
-   Alta;
-   Ultra Alta.

A classificação determina:

-   esforço esperado;
-   nível de revisão;
-   executor adequado.

------------------------------------------------------------------------

# 4. Decisão Humana

Algumas decisões precisam de aprovação.

Exemplos:

-   escolha de arquitetura;
-   mudança de tecnologia;
-   alteração de regras de negócio;
-   mudanças de contrato público.

O Executor não deve tomar essas decisões.

------------------------------------------------------------------------

# 5. Criação do Handoff

O Gerente cria uma tarefa estruturada contendo:

-   objetivo;
-   contexto;
-   arquivos permitidos;
-   regras;
-   critérios de aceite;
-   testes obrigatórios;
-   formato de retorno.

A tarefa deve ser autocontida.

------------------------------------------------------------------------

# 6. Escolha do Executor

Regra recomendada:

## Executor Flash

Para:

-   pequenas alterações;
-   documentação;
-   testes;
-   correções isoladas;
-   tarefas bem definidas.

## Executor Pro

Para:

-   arquitetura;
-   grandes refatorações;
-   problemas complexos;
-   migrações;
-   análises difíceis.

------------------------------------------------------------------------

# 7. Execução

O Executor:

-   lê a tarefa;
-   altera somente o necessário;
-   executa testes;
-   registra problemas;
-   retorna o resultado.

O Executor não amplia o escopo.

------------------------------------------------------------------------

# 8. Revisão

O Gerente verifica:

-   se a tarefa foi cumprida;
-   se arquivos corretos foram alterados;
-   se testes passaram;
-   se riscos foram identificados;
-   se o resultado atende ao objetivo.

A revisão é independente da execução.

------------------------------------------------------------------------

# 9. Registro Histórico

Cada ciclo deve gerar rastreabilidade:

-   tarefa criada;
-   executor utilizado;
-   alterações realizadas;
-   testes executados;
-   resultado;
-   decisões tomadas.

------------------------------------------------------------------------

# Exemplo Real --- StreamRank Lab

Fluxo validado:

    Gerente DeepSeek Pro

            ↓

    TASK-008
    Score de ranking

            ↓

    Executor Flash

            ↓

    Implementação

            ↓

    53 testes verdes

            ↓

    Revisão do Gerente

            ↓

    APROVADO

------------------------------------------------------------------------

# Princípios

## Pequenas tarefas

Grandes objetivos devem ser divididos.

## Revisão obrigatória

Executar não significa estar aprovado.

## Histórico permanente

Toda decisão importante deve ser registrada.

## Separação de papéis

Planejamento e implementação não devem ficar no mesmo agente.

------------------------------------------------------------------------

# Objetivo Final

Criar um processo semelhante a uma equipe profissional:

Humano: Produto e decisões.

Gerente: Arquitetura e coordenação.

Executor: Implementação.

Validação: Qualidade.
