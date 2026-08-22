# Gestão de skills no Hermes

## Fonte canônica

As skills deste framework vivem em:

```text
skills/software-development/<nome>/SKILL.md
```

Profiles do Hermes devem usar links simbólicos para essas pastas. Não copie versões divergentes para cada profile.

## Política

- Skill disponível não significa skill carregada.
- Adote apenas skills que resolvam problema real e tenham escopo discriminante.
- Regras de identidade/modelo ficam no SOUL/profile, não numa skill genérica.
- Procedimentos condicionais extensos ficam em `references/` e são lidos apenas quando aplicáveis.
- Atualizações devem mostrar o diff, preservar mudanças locais, validar e ser aprovadas antes de publicação.

## Validação

Para cada skill alterada:

1. validar frontmatter e nome;
2. confirmar que referências ligadas existem;
3. procurar duplicação ou regra específica de projeto/modelo;
4. testar o comportamento ou invariantes relevantes;
5. revisar o diff e o estado Git antes de commit/push.

No Hermes, confirme os links e a descoberta pelo comando de listagem de skills da versão instalada.

## Revisão periódica por evidência

A criação automática nativa do Hermes permanece desativada (`skills.creation_nudge_interval: 0`), pois sua cadência acompanha iterações de ferramentas, não etapas aceitas. O framework usa um gate próprio ligado ao evento durável `kanban_task_completed`:

- cada quatro conclusões distintas cria uma revisão;
- `[SKILL-REVIEW:CRITICAL]` antecipa a revisão para uma falha crítica;
- `[PHASE-COMPLETE]` fecha o lote no limite de fase;
- `[SKILL-REVIEW:IGNORE]` exclui tarefas administrativas;
- resumos não são persistidos pelo gate; somente IDs e metadados de roteamento;
- a revisão roda em `executor-gpt`, modelo Sol, esforço `xhigh`, com `skill-evolution-review` carregada;
- o revisor grava relatório e patch somente na área de staging e solicita revisão;
- publicação exige comando explícito com `--approved`, validação em cópia temporária e backup dos arquivos-alvo.

`ultra` não é a cadência padrão. Ele deve ser escolhido manualmente somente para contradição entre skills, segurança/dados críticos, mudança de governança ou consolidação arquitetural ambígua.

Estado e propostas ficam fora do Git em `~/.hermes/automation/skill-review/`. O gatilho nunca versiona sessões, logs, memórias, credenciais ou conteúdo bruto das tarefas.
