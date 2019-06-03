# ExampleJapanese


todo
- get the server running on a daemon
- sentence difficulty rating based on kanji level
- cap results to 100 lines

did
- build website frontend


systemd notes

where to make the file
/etc/systemd/system

snippits

> systemctl list-units | grep .service
> systemctl status $service
> sudo systemctl disable $service
> sudo systemctl enable $service
> sudo systemctl stop $service
> sudo systemctl start $service
> sudo systemctl restart $service
> systemctl --failed
