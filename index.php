<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

if(isset($_POST['send'])){

    $apiKey = "jafzKPrcM14P747f7pcZCslvUUzC8h";
    $sender = "919702974993";

    $number = trim($_POST['number']);
    $type = isset($_POST['type']) ? $_POST['type'] : '';

    $endpoint = "";
    $data = [];

    if($type == "text"){

        $endpoint = "https://ads.alixdeal.online/send-message";

        $data = [
            "api_key" => $apiKey,
            "sender" => $sender,
            "number" => $number,
            "message" => $_POST['message']
        ];
    }

    elseif($type == "image"){

        $endpoint = "https://ads.alixdeal.online/send-media";

        $data = [
            "api_key" => $apiKey,
            "sender" => $sender,
            "number" => $number,
            "media_type" => "image",
            "caption" => $_POST['caption'],
            "url" => $_POST['image_url']
        ];
    }

    elseif($type == "location"){

        $endpoint = "https://ads.alixdeal.online/send-location";

        $data = [
            "api_key" => $apiKey,
            "sender" => $sender,
            "number" => $number,
            "latitude" => $_POST['latitude'],
            "longitude" => $_POST['longitude']
        ];
    }

    // 🔥 Check if endpoint valid
    if($endpoint != ""){

        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $endpoint);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json'
        ]);

        $response = curl_exec($ch);
        curl_close($ch);

        $responseMessage = $response;

    } else {
        $responseMessage = "Invalid Type Selected!";
    }
}
?>