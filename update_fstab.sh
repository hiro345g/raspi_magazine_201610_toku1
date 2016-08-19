#!/bin/sh

f="/var/ramdisk"
# /var/ramdiskディレクトリー作成
# 所有者 pi、所有グループ pi を指定
if [ ! -e ${f} ]; then
  mkdir ${f}
  chown pi.pi ${f}
fi

# 空行追加
sh -c "echo '' >> /etc/fstab"
# /var/ramdiskの設定追加
sh -c "echo 'tmpfs ${f} tmpfs defaults,uid=1000,gid=1000,size=128m,noatime,mode=1755 0 0' >> /etc/fstab"

