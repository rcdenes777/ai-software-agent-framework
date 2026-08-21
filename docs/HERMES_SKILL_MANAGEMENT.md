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
