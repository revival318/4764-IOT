package com.example.speechrecognition;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.os.Bundle;
import android.speech.RecognizerIntent;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageView;
import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;


public class MainActivity<OkHttpClient, CustomRunnable> extends AppCompatActivity {

    ImageView speachButton;
    EditText speachText,Response;

    private static final int RECOGNIZER_RESULT = 1;

    @SuppressLint("MissingInflatedId")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        speachButton = findViewById(R.id.imageView);
        speachText = findViewById(R.id.editTextTextPersonName2);
        Response = findViewById(R.id.Response);

        speachButton.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view) {

                Intent speachIntent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
                speachIntent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
                speachIntent.putExtra(RecognizerIntent.EXTRA_PROMPT,"Speach to text");
                startActivityForResult(speachIntent,RECOGNIZER_RESULT);
            }
        });

    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {

        if (requestCode == RECOGNIZER_RESULT && resultCode == RESULT_OK){
            ArrayList<String> matches = data.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);
            speachText.setText(matches.get(0));
            new Thread(){
                @Override
                public void run() {
                        String response = sendMessage(String.valueOf(matches));
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                Response.setText(response);
                            }
                        });
                    }
            }.start();
        }
    }

    public String sendMessage (String message) {
        try {
            URL url = new URL("https://e00b-160-39-182-25.ngrok.io");
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("POST");
            conn.setDoInput(true);
            conn.setDoOutput(true);
            //conn.setConnectTimeout(30000);
            //conn.setReadTimeout(60000);

            String cmd = message.toLowerCase();

            if (cmd.contains("on")) {
                conn.setRequestProperty("Display", "on");
            } else if (cmd.contains("off")) {
                conn.setRequestProperty("Display", "off");
            } else if (cmd.contains("time")) {
                conn.setRequestProperty("Display", "time");
            } else {
                conn.setRequestProperty("Spoken_message", cmd);
            }


            conn.setDoOutput(true);
            OutputStream os = conn.getOutputStream();
            os.write(("?" + cmd).getBytes(StandardCharsets.UTF_8));

            os.flush();
            os.close();

            InputStream is = new BufferedInputStream(conn.getInputStream());
            BufferedReader bf = new BufferedReader(new InputStreamReader(
                    is, "UTF-8"), 8);
            StringBuilder sb = new StringBuilder();
            String line = "";
            while ((line = bf.readLine()) != null) {
                sb.append(line + "\n");
            }
            is.close();
            if (conn != null) {
                conn.disconnect();
            }
            String res = sb.toString();
            return res;
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        return "Error";
        }
}


