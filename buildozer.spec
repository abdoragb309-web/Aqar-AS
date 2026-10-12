[app]

title = Aqar AS

package.name = aqaras

package.domain = org.dezel

source.dir = .

source.include_exts = py,png,jpg,jpeg,kv,atlas

version = 0.1.0

requirements = python3,kivy

orientation = portrait

fullscreen = 0

[buildozer]

log_level = 2

warn_on_root = 1

[app:android]

android.permissions = INTERNET

android.api = 35

android.minapi = 23

android.archs = arm64-v8a

android.accept_sdk_license = True
