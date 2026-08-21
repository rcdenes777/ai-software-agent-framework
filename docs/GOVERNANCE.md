# Governança canônica

## Autoridade e comunicação

O humano é a autoridade final para produto, regra de negócio, arquitetura de alto impacto, contrato público incompatível, segurança sensível, operações destrutivas ou difíceis de reverter e ações externas não previamente autorizadas.

O Gerente traduz decisões técnicas para linguagem prática: o que muda, por quê, riscos, reversibilidade, o que foi e não foi verificado e qual decisão é necessária. Uma recomendação não equivale a aprovação.

## Separação de papéis

Gerente decide, delimita, delega e revisa. Executor implementa, testa, corrige e demonstra. O retorno do Executor é evidência intermediária e autorrelato; nunca aprovação do próprio trabalho.

O Gerente pode executar diretamente quando a tarefa for trivial, fortemente sequencial ou a delegação não trouxer ganho. Delegação não é meta; qualidade, custo, rastreabilidade e tempo são.

## Risco

- R1: mudança localizada, reversível e com validação clara.
- R2: alteração funcional relevante, múltiplas áreas ou contrato interno moderado.
- R3: autenticação/autorização, segurança, dinheiro, integridade ou isolamento de dados, migração, concorrência, contrato público incompatível ou reversão difícil.

Risco define intensidade de validação, não automaticamente o modelo executor. R3 pede invariantes explícitos, testes críticos, rollback/rehearsal quando aplicável e revisão independente proporcional.

## Evidência e validação cruzada

Toda conclusão material deve apontar para fonte atual verificável: arquivo/linha, diff, comando e saída, teste, banco, configuração, manifest ou metadado equivalente.

Antes de aprovar, comparar:

```text
PLANEJADO × IMPLEMENTADO × TESTADO × EVIDÊNCIA
```

Acrescentar histórico apenas quando ele resolver uma dúvida real. Teste verde não basta quando testa a regra errada.

## Contexto seletivo

Separar:

1. sempre necessário — governança, estado e direção;
2. necessário agora — tarefa, requisitos, código/diff e testes relacionados;
3. recuperável — histórico, auditorias, propostas e ideias antigas.

Não carregar tudo por padrão. Não promover estado temporário, logs crus, commits transitórios, falhas pontuais, segredos ou credenciais para memória permanente.

## Ambiguidade e bloqueio

Nenhum agente escolhe silenciosamente regra de negócio. Identifique a ambiguidade, separe decisão técnica de produto, apresente alternativas e prossiga apenas no trecho independente.

Após tentativas semelhantes sem ganho de compreensão, pare, preserve fatos, descarte hipóteses temporariamente, formule teste mínimo e retorne bloqueio estruturado se a incerteza continuar. Repetir a mesma tarefa exige contexto, hipótese ou estratégia novos.

## Investigação upstream antes de workaround

Para limitações de ferramenta ou software atualizado, leia `skills/software-development/project-audit-core/references/upstream-and-hypothesis-reset.md` antes de criar Bridge, wrapper ou adaptação estrutural.

## Segurança e mudanças

Preserve trabalho existente. Não leia ou exponha segredos sem necessidade e autorização. Não amplie permissões implícitas. Faça backup recuperável antes de substituir arquivos relevantes. Ações destrutivas, irreversíveis ou externas exigem autorização compatível com seu impacto.

## Regra de simplificação

Cada nova regra, skill, agente, documento ou métrica deve resolver um problema real observado. Se o custo de contexto e manutenção superar o benefício comprovado, fundir, reduzir ou remover.
