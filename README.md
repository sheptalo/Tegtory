# Tegtory
<p>
    <a href="https://github.com/sheptalo/Tegtory/pulse" alt="Activity">
        <img src="https://img.shields.io/github/commit-activity/m/sheptalo/Tegtory"  alt=""/></a>
    <a href="https://github.com/sheptalo/Tegtory/discussions" alt="Discussions">
        <img src="https://img.shields.io/github/discussions/sheptalo/Tegtory"  alt=""/></a>
</p>
    
[![Tegtory functions](https://github.com/sheptalo/Tegtory/actions/workflows/run.tests.yml/badge.svg)](https://github.com/sheptalo/Tegtory/actions/workflows/run.tests.yml)

## Описание и функционал

Создай свою фабрику и подними ее в вершины таблицы лидеров вместе с друзьями.

Продавай свою продукцию в самые подходящие моменты

Устал на фабрике? Развлекись в других ботах этого семейства ведь прогресс синхронизируется и заработав миллион в казино ты получишь его здесь

# Нашел баг? Создай Issue!

Если столкнулся с багом, сообщи об этом. Он будет исправлен в ближайшее время, ты получишь бонус и все будет классно.

Если ты используешь баги в личных целях будет бан.

## Architecture

```text
├──common
├──docker
├──domain
│  ├───commands
│  ├───context
│  ├───entity
│  ├───events
│  ├───interfaces
│  ├───policies
│  ├───queries
│  ├───services
│  └───use_cases
│      ├───commands
│      └───queries
├──infrastructure
│  ├───events
│  └───repositories
├──presentors
│  ├───aiogram # main tegtory specific modules
│  ├───mynox # mynox specific modules
│  └───shared # shared modules
├──static
│  └───tegtory
└──tests
    ├───entity
    ├───presentors
    └───use_cases
```

---
