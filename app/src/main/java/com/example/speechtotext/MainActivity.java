package com.example.speechtotext;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.annotation.SuppressLint;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.ActivityNotFoundException;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.provider.Settings;
import android.speech.RecognizerIntent;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Spinner;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Locale;

public class MainActivity extends AppCompatActivity {

    private Button recordButton;
    private TextView speechOutput;
    private Switch saveSwitch;
    private static final int WRITE_TO_FILE = 1;
    private static final int VOICE_RECOGNITION_CODE = 100;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        recordButton = (Button) findViewById(R.id.recordVoiceBtn);
        speechOutput = (TextView) findViewById(R.id.textOutput);
        saveSwitch = (Switch) findViewById(R.id.saveTextSwitch);


        recordButton.setText("Click and Start Talking");//


        recordButton.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {


                Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
                intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                        RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
                intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault());
                intent.putExtra(RecognizerIntent.EXTRA_PROMPT, "Speak");
                try{
                    startActivityForResult(intent, VOICE_RECOGNITION_CODE);



                } catch (ActivityNotFoundException e) {
                    Toast.makeText(getApplicationContext(), "Device Not Supported",
                            Toast.LENGTH_SHORT).show();
                }


            }
        });


    }

    /*
    private void checkPermission() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            if (!(ContextCompat.checkSelfPermission(this,
                    Manifest.permission.RECORD_AUDIO) == PackageManager.PERMISSION_GRANTED)) {
                Intent intent = new Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS,
                        Uri.parse("package:" + getPackageName()));
                startActivity(intent);
                finish();
            }
        }
    }
     */


    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        switch (requestCode){
            case VOICE_RECOGNITION_CODE: {
                if(resultCode == Activity.RESULT_OK && data != null)
                {
                    ArrayList<String> result = data.getStringArrayListExtra(
                            RecognizerIntent.EXTRA_RESULTS);
                    if(result.size() == 0 )
                    {
                        RuntimeException e = new RuntimeException();
                        throw e;
                    }
                    speechOutput.setText(result.get(0));

                    Message msg = Message.obtain();
                    msg.what = WRITE_TO_FILE;
                    msg.obj = result.get(0);
                    returnMsgHandler.sendMessage(msg);

                }

                break;
            }
        }
    }


    Handler returnMsgHandler = new Handler() {
        public void handleMessage(Message msg) {
            if(msg.what == WRITE_TO_FILE)
            {
                if(saveSwitch.isChecked())
                {
                    try {
                        FileOutputStream fileOutputStream = openFileOutput(
                                "conversion.txt", MODE_PRIVATE);
                        fileOutputStream.write(msg.obj.toString().getBytes());
                        fileOutputStream.close();
                    }
                    catch(IOException e)
                    {
                        e.printStackTrace();
                    }
                }
            }
        }
    };
}
