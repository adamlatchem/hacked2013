<?php

function_exists('curl_init');
 include_once 'windowsphonepush.php';
 
echo 'Push Notification API for Windows Phone';

//Device UUID
$UUID = file_get_contents('uuid_dev'); 
echo $UUID;

$uri="http://db3.notify.live.net/throttledthirdparty/01.00/".$UUID; //uri sended by Microsoft plateform
$notif=new WindowsPhonePushNotification($uri);
$result = $notif->push_toast("Some One is at the Door","Go open it Duh!!");

echo $result;
?>