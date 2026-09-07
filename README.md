# DebRepo

Автоматический APT-репозиторий для Sileo/Cydia от RenG1n.

## Как пользоваться

Единственное действие: загружай `.deb` в папку `pool/` через GitHub и делай **Commit changes**.

GitHub Actions автоматически:
- находит все `.deb` в `pool/`;
- читает `DEBIAN/control`;
- создаёт `Packages`;
- создаёт `Packages.gz`;
- создаёт `Release`;
- публикует репозиторий через GitHub Pages.

После настройки Pages адрес будет:

https://reng1n.github.io/DebRepo/

`Packages`, `Packages.gz` и `Release` вручную редактировать не нужно.

Важно: GitHub Actions запускается после commit. Сам файл `.deb` должен быть разрешён к распространению. Чужие твики не следует перепаковывать или распространять без соответствующего разрешения.
