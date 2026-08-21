# AI Software Agent Framework

Framework enxuto de governança, skills e templates para desenvolvimento de software assistido por IA.

## Fluxo canônico

```text
Humano
  ↓
Gerente — entende, decide, delimita, delega e revisa
  ↓
Executor — implementa, testa, corrige e demonstra
  ↓
Gerente — valida fontes atuais e decide
  ↓
Humano — aprova decisões reservadas
```

Gerente e Executor são papéis, não modelos fixos. O modelo mais econômico comprovadamente capaz deve executar trabalho delimitado; risco e evidência determinam a intensidade da revisão e eventual escalonamento.

## Fontes canônicas

- `docs/GOVERNANCE.md`: regras permanentes e limites de autoridade.
- `docs/ARCHITECTURE.md`: papéis, fluxo, roteamento e distribuição de regras.
- `skills/software-development/`: procedimentos reutilizáveis carregados sob demanda.
- `templates/`: registros portáteis de projeto, tarefa, handoff e decisão humana.
- `docs/HISTORY.md`: decisões históricas que explicam a arquitetura atual, sem reger a execução.

## Princípios

- Evidência atual prevalece sobre memória, histórico e autorrelato.
- Executor não aprova o próprio trabalho.
- Contexto disponível não significa contexto carregado.
- Complexidade orienta decomposição; risco orienta validação.
- Workarounds exigem prova de que a alternativa nativa atual não atende.
- Toda nova regra ou artefato deve resolver um problema real observado.

Status: em validação contínua em projetos reais.
