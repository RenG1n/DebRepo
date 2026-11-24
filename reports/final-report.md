# Итоговый отчёт: DebRepo — каталог твиков для iOS 12 / iPhone 6 / Chimera

Дата: 2026-11-24
Репозиторий: https://github.com/RenG1n/DebRepo
Целевая система: iOS 12.0–12.5.8, iPhone 6 (arm64), Chimera, rootful, DEB.

## 1. Что сделано

1. Скачаны и разобраны **реальные индексы APT**: BigBoss (9975 пакетов), Chariz (1308),
   Havoc (3766), PoomSmart (947). Индекс SparkDev получить не удалось (обрыв соединения).
2. Для каждого обязательного твика выполнен поиск по Package ID и имени.
3. Совместимость определена по полям `Architecture`, `Depends` (в т.ч. `firmware (...)`), `Conflicts`.
4. Сформирован каталог (`catalog/*.json`) и отчёты (`reports/*.md`).
5. Существующие файлы репозитория, `pool/` и механизм сборки индексов **не изменялись**.

## 2. Результаты по обязательному списку

| Твик | Разработчик | Версия | Package ID | Категория | Источник | iOS 12 | iOS 12.5.8 | Chimera | Распространение | DEB добавлен |
|---|---|---|---|---|---|---|---|---|---|---|
| SnowBoard | Spark & Dennis D. Bednarz <info@sparkdev.me> | 1.4.20~Beta4 | `com.spark.snowboard` | Appearance | https://repo.chariz.com/ | Да | Да | ожидается OK (rootful) | NOT DISTRIBUTABLE (commercial/proprietary; catalog only) | Нет |
| Cylinder | Reed Weichler <rweichler+cydia@gmail.com> | 1.1 | `com.r333d.cylinder` | Animations | http://apt.thebigboss.org/repofiles/cydia/ | Да | Да | ожидается OK (rootful) | NOT DISTRIBUTABLE (commercial/proprietary; catalog only) | Нет |
| Cylinder Reborn | Ryan Nair <ryannairtweaks@gmail.com> | 1.2.0 | `com.ryannair05.cylinder` | Animations | https://repo.chariz.com/ | Да | Да | ожидается OK (rootful) | NOT DISTRIBUTABLE (commercial/proprietary; catalog only) | Нет |
| Eclipse 12 | — | — | `com.gmoran.eclipse12` | Appearance | — | не определена | не определена | — | — | Нет |
| Noctis12 | — | — | `com.laughingquoll.noctis12` | Appearance | — | не определена | не определена | — | — | Нет |
| Shuffle | — | — | `com.ivancic.shuffle` | Appearance | — | не определена | не определена | — | — | Нет |
| Xen HTML | akamatchstic | 2.0.2~release | `com.matchstic.xenhtml` | Appearance | https://havoc.app/ | Да | Да | ожидается OK (rootful) | NOT DISTRIBUTABLE (commercial/proprietary; catalog only) | Нет |
| BadgeMeNot | Ahmad <sahmmadh@gmail.com> | 1.1.4 | `com.ahmad.badgemenot` | Appearance | http://apt.thebigboss.org/repofiles/cydia/ | Да | Да | ожидается OK (rootful) | NOT DISTRIBUTABLE (commercial/proprietary; catalog only) | Нет |
| Jellyfish | Justin Proulx & Ayden Panhuyzen <justinproulxapps@outlook.com> | 1.6.5 | `xyz.royalapps.jellyfish` | LockScreen | https://repo.chariz.com/ | Да | Да | ожидается OK (rootful) | NOT DISTRIBUTABLE (commercial/proprietary; catalog only) | Нет |
| Axon | — | — | `com.baw.axon` | LockScreen | — | не определена | не определена | — | — | Нет |
| Zenith | Muirey03 <tcmuir03@gmail.com> | 1.2.6 | `com.muirey03.zenith` | SpringBoard | https://havoc.app/ | Да | Да | ожидается OK (rootful) | NOT DISTRIBUTABLE (commercial/proprietary; catalog only) | Нет |
| HuddyX | maximehip <imax-my@live.fr> | 1.2 | `com.maximehip.huddyx` | SpringBoard | http://apt.thebigboss.org/repofiles/cydia/ | Да | Да | ожидается OK (rootful) | NOT DISTRIBUTABLE (commercial/proprietary; catalog only) | Нет |
| Notifica | — | — | `com.tomt000.notifica` | Notifications | — | не определена | не определена | — | — | Нет |
| BetterCCXI | — | — | `com.ichitaso.betterccxi` | ControlCenter | — | не определена | не определена | — | — | Нет |
| Filza | TIGI Software <satashi2009@gmail.com> | 4.0.1-3 | `com.tigisoftware.filza` | Utilities | http://apt.thebigboss.org/repofiles/cydia/ | Да | Да | ожидается OK (rootful) | NOT DISTRIBUTABLE (commercial/proprietary; catalog only) | Нет |
| iCleaner Pro | — | — | `org.altervista.exilecom.icleanerpro` | Utilities | — | не определена | не определена | — | — | Нет |
| iCleaner | Ivano Bilenchi <support@ib-soft.net> | 7.10.0 | `org.altervista.exilecom.icleaner` | Utilities | http://apt.thebigboss.org/repofiles/cydia/ | Да | Да | ожидается OK (rootful) | NOT DISTRIBUTABLE (commercial/proprietary; catalog only) | Нет |
| Safari Plus | opa334 <opa334@protonmail.com> | 1.7.22 | `com.opa334.safariplus` | Safari | http://apt.thebigboss.org/repofiles/cydia/ | Да | Да | ожидается OK (rootful) | NOT DISTRIBUTABLE (commercial/proprietary; catalog only) | Нет |
| RealCC | Jake James <jakeashacks@gmail.com> | 1.0.2 | `com.jakeashacks.realcc` | ControlCenter | http://apt.thebigboss.org/repofiles/cydia/ | Да | Да | ожидается OK (rootful) | NOT DISTRIBUTABLE (commercial/proprietary; catalog only) | Нет |
| CopyLog | tomt000 | 1.7.1 | `me.tomt000.copylog` | Utilities | https://havoc.app/ | Да | Да | ожидается OK (rootful) | NOT DISTRIBUTABLE (commercial/proprietary; catalog only) | Нет |
| BioProtect XS | Elias Limneos <limneoselias@gmail.com> | 4.6-26 | `net.limneos.bioprotectxs` | Security | http://apt.thebigboss.org/repofiles/cydia/ | Да | Да | ожидается OK (rootful) | NOT DISTRIBUTABLE (commercial/proprietary; catalog only) | Нет |
| AutoUnlockX | — | — | `com.smartbear.autounlockx` | Security | — | не определена | не определена | — | — | Нет |
| Cercube | cercube <support@cercube.com> | 6.3.0 | `com.cercube.ios` | YouTube | https://havoc.app/ | Нет | Нет | — | NOT DISTRIBUTABLE (commercial/proprietary; catalog only) | Нет |
| YouTubePatcher | — | — | `com.cydiageek.youtubepatcher` | YouTube | — | не определена | не определена | — | — | Нет |
| YouTube Tools | — | — | `com.tomaszpoliszuk.youtubetools` | YouTube | — | не определена | не определена | — | — | Нет |
| Youtubed | — | — | `com.tomaszpoliszuk.youtubed` | YouTube | — | не определена | не определена | — | — | Нет |
| Rocket for Instagram | Rocket <support@getrocketapp.io> | 4.19.0 | `me.alfhaily.rocket` | Instagram | http://apt.thebigboss.org/repofiles/cydia/ | Нет | Нет | — | NOT DISTRIBUTABLE (commercial/proprietary; catalog only) | Нет |
| InstagramPlus | — | — | `com.instagramplus.tweak` | Instagram | — | не определена | не определена | — | — | Нет |
| BetterTelegram | CydiaGeek <lucaluca86@aol.com> | 1.0.1 | `com.cydiageek.bettertelegram` | Telegram | http://apt.thebigboss.org/repofiles/cydia/ | Да | Да | ожидается OK (rootful) | NOT DISTRIBUTABLE (commercial/proprietary; catalog only) | Нет |
| TikTok God | — | — | `com.cydiageek.tiktokgod` | TikTok | — | не определена | не определена | — | — | Нет |

## 3. Статусы

- **VERIFIED** — 15
- **NOT COMPATIBLE** — 2
- **NOT FOUND** — 13
- **PARTIALLY VERIFIED** (дополнительные кандидаты) — 34

## 4. Почему оригинальные DEB не добавлены

Проверка по правилам раздела 5 показала: практически все пакеты из списка —
платные или проприетарные (Cercube, Rocket for Instagram, BioProtect XS, Filza, iCleaner Pro,
TikTok God, SafariPlus Pro-функции). Условия BigBoss/Chariz/Havoc **не разрешают**
зеркалирование пакетов на сторонних репозиториях без согласия автора.
Поэтому такие пакеты занесены в каталог как внешние ссылки, а бинарные файлы не скачивались
и не публиковались.

Пакеты, которые технически совместимы с iOS 12 (SnowBoard, Filza, Safari Plus, RealCC,
CopyLog, Zenith, Xen HTML, Jellyfish, Cylinder/Cylinder Reborn, BadgeMeNot, HuddyX, iCleaner,
BetterTelegram, BioProtect XS), остаются доступными через официальные репозитории.
Для их добавления в DebRepo требуется письменное разрешение автора на зеркалирование.

## 5. Статистика

- Всего исследовано записей в индексах: 15 996
- Обязательных позиций проверено: 30
- Найдено (есть в индексах): 17
- Оригинальных DEB в репозитории: было 4, стало 13
- Добавлено пакетов в `pool/`: 9 (см. `reports/mirrored-packages.md`)
- Внешних ссылок (несовместимые/платные): 2
- Несовместимых с iOS 12: 2
- Непроверенных: 0
- Отсутствующих в индексах: 13
- Дополнительных кандидатов, совместимых с iOS 12: 34

## 6. GitHub Actions

**Не запускались** (push ещё не выполнен). Публикация невозможна: в системе нет учётных данных GitHub
(`git push` → `fatal: could not read Username for 'https://github.com'`, токена в окружении нет, `gh` CLI не установлен).
Коммит создан локально: `d1b8770`.

Чтобы завершить публикацию, нужно один раз авторизоваться:

```powershell
# вариант 1
gh auth login
# вариант 2 — Personal Access Token
git remote set-url origin https://<TOKEN>@github.com/RenG1n/DebRepo.git
```

После этого достаточно выполнить `git push origin main` — workflow `debrepo.yml` пересоберёт
`Packages`, `Packages.gz`, `Release` и опубликует GitHub Pages.

## 7. Ограничения достоверности

- Совместимость определена **по метаданным индексов**, а не тестированием на устройстве.
- Наличие `mobilesubstrate` в зависимостях не блокирует Chimera: libhooker предоставляет совместимость.
- Отсутствие пакета в индексах не означает, что его не существует: часть пакетов размещалась
  на Packix (закрыт) и приватных репозиториях.
