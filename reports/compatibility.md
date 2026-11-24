# Совместимость с iOS 12 / 12.5.8 — iPhone 6 (arm64, Chimera, rootful)

Данные получены из реальных индексов APT (BigBoss, Chariz, Havoc, PoomSmart).
Проверялись поля Architecture, Depends (в т.ч. firmware ...), Conflicts.

| Твик | Package | Версия | Архитектура | iOS min | Статус |
|---|---|---|---|---|---|
| SnowBoard | `com.spark.snowboard` | 1.4.20~Beta4 | iphoneos-arm | - | VERIFIED |
| Cylinder | `com.r333d.cylinder` | 1.1 | iphoneos-arm | 3.0 | VERIFIED |
| Cylinder Reborn | `com.ryannair05.cylinder` | 1.2.0 | iphoneos-arm | 11.0 | VERIFIED |
| Eclipse 12 | `com.gmoran.eclipse12` | - | - | - | NOT FOUND |
| Noctis12 | `com.laughingquoll.noctis12` | - | - | - | NOT FOUND |
| Jellyfish | `xyz.royalapps.jellyfish` | 1.6.5 | iphoneos-arm | 11.0 | VERIFIED |
| Axon | `com.baw.axon` | - | - | - | NOT FOUND |
| Zenith | `com.muirey03.zenith` | 1.2.6 | iphoneos-arm | - | VERIFIED |
| HuddyX | `com.maximehip.huddyx` | 1.2 | iphoneos-arm | 12.0 | VERIFIED |
| Notifica | `com.tomt000.notifica` | - | - | - | NOT FOUND |
| Shuffle | `com.ivancic.shuffle` | - | - | - | NOT FOUND |
| BetterCCXI | `com.ichitaso.betterccxi` | - | - | - | NOT FOUND |
| Xen HTML | `com.matchstic.xenhtml` | 2.0.2~release | iphoneos-arm | 11.0 | VERIFIED |
| BadgeMeNot | `com.ahmad.badgemenot` | 1.1.4 | iphoneos-arm | 12.0 | VERIFIED |
| Filza | `com.tigisoftware.filza` | 4.0.1-3 | iphoneos-arm | 7.0 | VERIFIED |
| iCleaner Pro | `org.altervista.exilecom.icleanerpro` | - | - | - | NOT FOUND |
| iCleaner | `org.altervista.exilecom.icleaner` | 7.10.0 | iphoneos-arm | - | VERIFIED |
| Safari Plus | `com.opa334.safariplus` | 1.7.22 | iphoneos-arm | 11.0 | VERIFIED |
| RealCC | `com.jakeashacks.realcc` | 1.0.2 | iphoneos-arm | 11.0 | VERIFIED |
| CopyLog | `me.tomt000.copylog` | 1.7.1 | iphoneos-arm | - | VERIFIED |
| BioProtect XS | `net.limneos.bioprotectxs` | 4.6-26 | iphoneos-arm | 12.0 | VERIFIED |
| AutoUnlockX | `com.smartbear.autounlockx` | - | - | - | NOT FOUND |
| Cercube | `com.cercube.ios` | 6.3.0 | iphoneos-arm | 15.0 | NOT COMPATIBLE |
| YouTubePatcher | `com.cydiageek.youtubepatcher` | - | - | - | NOT FOUND |
| YouTube Tools | `com.tomaszpoliszuk.youtubetools` | - | - | - | NOT FOUND |
| Youtubed | `com.tomaszpoliszuk.youtubed` | - | - | - | NOT FOUND |
| Rocket for Instagram | `me.alfhaily.rocket` | 4.19.0 | iphoneos-arm | 15.0 | NOT COMPATIBLE |
| InstagramPlus | `com.instagramplus.tweak` | - | - | - | NOT FOUND |
| BetterTelegram | `com.cydiageek.bettertelegram` | 1.0.1 | iphoneos-arm | 9.0 | VERIFIED |
| TikTok God | `com.cydiageek.tiktokgod` | - | - | - | NOT FOUND |

## Замечания

- iphoneos-arm = rootful (подходит для Chimera). iphoneos-arm64 = rootless (не подходит).
- Chimera использует libhooker, который предоставляет mobilesubstrate; зависимость от mobilesubstrate сама по себе не блокирует установку.
- Совместимость определена по метаданным индекса. Реальная работа на устройстве не проверялась.
