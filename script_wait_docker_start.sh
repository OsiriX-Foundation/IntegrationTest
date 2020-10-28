#!/bin/bash


docker_name=("kheopsreverseproxy" "pacsauthorizationproxy" "kheopsauthorization" "pacsarc" "pacspostgres" "keycloak" "kheopsdicomwebproxy"\
            "kheopszipper" "kheopsui" "kheopspostgres" "ldap")

docker_logs=("" "" "" "" "" "" "" "" "" "" "")

while true;
do
   i=0
   flag=false
   for dn in "${docker_name[@]}"
   do
      old_log=${docker_logs[$i]}
      log=$(docker logs --tail 1 $dn)

      if [ "$old_log" != "$log" ]; then 
         flag=true
      fi

      docker_logs[i]=$log
      i=$((i+1))
   done

   if [ $flag = true ];
   then
      echo "waiting 10 secondes..."
      sleep 10
   else
    break
   fi
done