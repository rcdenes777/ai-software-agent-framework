# Hermes Skill Management Guide

## Objetivo

Guia para criar, versionar e disponibilizar skills no Hermes Agent.

## Estrutura

Uma skill segue o formato:

    categoria/
    └── nome-da-skill/
        └── SKILL.md

Exemplo:

    software-development/
    └── project-manager-core/
        └── SKILL.md

## Fonte Git

Manter as skills no repositório:

    ~/Documentos/ai-software-agent-framework

Exemplo:

    skills/software-development/project-manager-core/SKILL.md

O Git é a fonte oficial.

## Local Hermes

O Hermes utiliza:

    ~/.hermes/skills/

Exemplo:

    ~/.hermes/skills/software-development/project-manager-core

## Integração

Criar link simbólico:

    ln -s ~/Documentos/ai-software-agent-framework/skills/software-development/project-manager-core ~/.hermes/skills/software-development/project-manager-core

## SKILL.md

Modelo:

``` yaml
---
name: nome-da-skill
description: Descrição curta da skill.
version: 1.0.0
author: AI Software Agent Framework
license: MIT
---
```

## Validação

Comando:

    hermes skills list

Esperado:

    nome-da-skill | categoria | local | local | enabled

## Fluxo completo

    Criar Skill no Git
    ↓
    Criar SKILL.md
    ↓
    Adicionar metadata Hermes
    ↓
    Criar link simbólico
    ↓
    hermes skills list
    ↓
    Testar
    ↓
    Commit
