# Arquitetura canônica Gerente–Executor

## Núcleo mínimo

```text
HUMANO
  │ objetivos, prioridades e decisões reservadas
  ▼
GERENTE
  │ tarefa autocontida, autorização e critérios de aceite
  ▼
EXECUTOR
  │ alterações, testes, evidências, riscos e bloqueios
  ▼
GERENTE
  │ verificação independente e decisão
  ├─ aprovar
  ├─ pedir correção
  ├─ escalar execução/revisão
  └─ solicitar decisão humana
```

Funções especializadas — testes, segurança, banco, migração ou revisão independente — são skills, checklists, ferramentas ou instâncias temporárias. Não precisam ser agentes permanentes.

## Responsabilidades

### Humano

Define produto, prioridades e decisões de alto impacto. Autoriza operações destrutivas, irreversíveis, externas ou fora do escopo concedido.

### Gerente

Mantém a visão global; confirma o estado atual; esclarece requisitos; controla escopo; classifica risco; decompõe; escolhe contexto e executor; define testes; delega; revisa evidências; procura omissões; decide correção, escalonamento ou conclusão.

### Executor

Executa somente o recorte autorizado; preserva trabalho alheio; testa; corrige; distingue fato de hipótese; reporta alterações, comandos, resultados, riscos, incertezas e o que não foi validado. Não redefine arquitetura, produto, escopo ou permissões.

## Roteamento

Começar pelo executor de menor custo já demonstrado como capaz para a classe de tarefa. Não usar “complexo = modelo caro” como regra. Escalar quando houver evidência concreta, como baixa confiança após teste mínimo, falhas repetidas, alto custo de reversão, risco crítico, contradição ou necessidade de contexto/capacidade não disponível.

Trabalho efêmero e delimitado pode usar delegação nativa. Trabalho que precisa sobreviver à sessão ou participar de um grafo usa coordenação durável, como Kanban. O mecanismo é escolha operacional; os papéis permanecem os mesmos.

## Distribuição das regras

- SOUL/profile: identidade e política de roteamento específica daquela equipe/modelo.
- Skills: procedimentos reutilizáveis e acionáveis.
- Governança: autoridade, segurança, risco e invariantes permanentes.
- Templates: contratos e registros preenchidos por projeto/tarefa.
- Histórico: explicação de decisões passadas, nunca verdade operacional atual.

## Fontes de verdade

1. Código, Git, bancos, testes e configuração efetiva atuais.
2. Documentação canônica atual do projeto.
3. Tarefa, handoff, status e decisões humanas atuais.
4. Governança e skills aplicáveis.
5. Memória curada.
6. Histórico de sessões e documentos antigos.
7. Inferência.

Quando uma fonte inferior puder mudar uma ação sobre código, Git, banco ou infraestrutura, confirme em fonte superior antes de agir.
