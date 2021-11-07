# devops-netology

First commit

Убрал из шаблона Terraform.gitignore. закоментированные строки и подписал что будет игнорироваться:

**/.terraform/*
Игнорировать содержимое папки .terraform расположенный в любом месте репозитория

*.tfstate
Игнорировать файлы с этим расширение
*.tfstate.*
Инорировать файлы у который в имени может встречать расширение .tfstate.

crash.log
игнорировать файл crash.log

*.tfvars
игнорировать файлы с этим расширением

override.tf
override.tf.json
*_override.tf
*_override.tf.json
Аналогично игнорировать указанные имена файлов и файлы с расширениями

.terraformrc
terraform.rc
Аналогично игнорировать указанные файлы

New line in the main branch