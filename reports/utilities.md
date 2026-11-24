# Системные утилиты — статус по 25 позициям

Цель: iOS 12.5.8, rootful, `iphoneos-arm`, iPhone 6.

## Высокий приоритет

| # | Утилита | Package | Версия | Статус | Примечание |
|---|---|---|---|---|---|
| 1 | Filza File Manager | `com.tigisoftware.filza` | 4.0.1-2 | Compatible | уже был в репозитории (10 МБ, обновление 4.0.1-3 не тянулось) |
| 2 | NewTerm 2 | `ws.hbang.newterm2` | 2.5 | Likely compatible | Chariz обрывает загрузку на ~14 КБ из 2 МБ |
| 3 | iCleaner Pro | `org.altervista.exilecom.icleanerpro` | — | Unknown | платная Pro-версия; бесплатный `icleaner` 7.10.0 уже в репозитории |
| 4 | Cr4shed | `com.muirey03.cr4shed` | 4.3.0 | Compatible | Havoc, 149 КБ |
| 5 | CocoaTop | `ru.domo.cocoatop64` | 2.2.3 | Compatible | BigBoss, 232 КБ |
| 6 | PowerSelector | `com.ichitaso.powerselector11` | 1.2.1 | Compatible | BigBoss, 192 КБ |
| 7 | AppSync Unified | `ai.akemi.appsyncunified` | 116.0 | Incompatible (rootful) | arm64/rootless; официальный репозиторий отдаёт HTTP 522 |
| 8 | Apple File Conduit 2 | `com.cannathea.afc2d-arm64` | 1.2.1 | Incompatible | только arm64-сборка |
| 9 | OpenSSH | `openssh` + server/client | 8.4-2 | Compatible | Bingner; см. предупреждение ниже |
| 10 | Apps Manager | `com.tigisoftware.appdatamanager` | 1.8.2-5 | Compatible | 2.5 МБ |
| 11 | Choicy | `com.opa334.choicy` | 1.5.4-2 | Compatible | требует altlist |
| 12 | Zebra | `xyz.willy.zebra` | 1.1.36 | Compatible | 8.4 МБ, официальный getzbra.com |

## Средний приоритет

| # | Утилита | Package | Версия | Статус |
|---|---|---|---|---|
| 13 | Batchomatic | `com.captinc.batchomatic` | 4.3.1 | Compatible |
| 14 | Frida | — | — | Unknown — нет rootful arm-сборки в доступных индексах |
| 15 | LLDB | `lldb-10` + `liblldb-10` | 10.0.0~svn | Compatible (диагностика) |
| 16 | Darwin CC Tools | `org.coolstar.cctools` | 895 | Compatible |
| 17 | ReProvision Reborn | `jp.soh.reprovision` | 0.8.4 | Likely compatible — 16 МБ, не докачано |
| 18 | WiFi Passwords | `com.malcolmhall.wifipasswords` | 3.0.1 | Compatible |
| 19 | GoodWiFi | — | — | Unknown — не найдено в индексах |
| 20 | Flex 3 | `com.johncoates.Flex3` | 3~EarlyAccess | Incompatible / платный — не зеркалировался |
| 21 | Succession | `com.samgisaninja.successionrestore` | 1.4.15 | Compatible |
| 22 | App Manager | `com.tigisoftware.appdatamanager` | 1.8.2-5 | Compatible (тот же пакет) |
| 23 | Cycript | `cycript` | 0.9.594 | Compatible |
| 24 | SSL Kill Switch 2 | — | — | Unknown — нет в доступных индексах |
| 25 | LocationFaker | `com.cunstuck.locationfakerx` | 2.9-1 | Likely compatible — 1.4 МБ, не докачано |

Дополнительно добавлены CLI-утилиты Bingner: `adv-cmds`, `top`, `rsync`.

## AppSync Unified — результат проверки

- Текущая сборка в `pool/`: версия **116.0**, архитектура **iphoneos-arm64** (rootless).
- Для iOS 12.5.8 и Chimera нужна **iphoneos-arm** (rootful) — текущая не установится.
- Официальный источник `https://cydia.akemi.ai/` возвращает **HTTP 522** (origin timeout) и по HTTPS, и по HTTP; альтернативные хосты (`apt.akemi.ai`, `repo.akemi.ai`) не резолвятся.
- **Замена не выполнена**: подходящей официальной сборки получить не удалось. Пакет не подделывался и не модифицировался.
- Рекомендация: повторить попытку позже, когда репозиторий akemi восстановится, и заменить файл на arm-сборку с проверкой SHA256.

## Предупреждения безопасности

- **OpenSSH**: открывает SSH-доступ к устройству (порт 22). Смените пароли `root` и `mobile` (по умолчанию `alpine`) сразу после установки, не выставляйте устройство в публичную сеть, используйте ключи вместо паролей.
- **SSL Kill Switch 2**: инструмент диагностики (отключает проверку сертификатов в приложениях), а не средство защиты. Не оставлять включённым постоянно — снижает безопасность TLS.
- **WiFi Passwords / CocoaTop / Cycript** требуют root-доступа и показывают чувствительные данные.
