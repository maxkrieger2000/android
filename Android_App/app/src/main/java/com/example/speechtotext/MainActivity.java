package com.example.speechtotext;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import android.Manifest;
import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.speech.RecognizerIntent;
import android.speech.SpeechRecognizer;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;

import com.microsoft.cognitiveservices.speech.CancellationDetails;
import com.microsoft.cognitiveservices.speech.ResultReason;
import com.microsoft.cognitiveservices.speech.SpeechConfig;
import com.microsoft.cognitiveservices.speech.SpeechRecognitionResult;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.net.URI;
import java.util.ArrayList;
import java.util.Locale;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Future;

public class MainActivity extends AppCompatActivity {

    private static final String TAG = "MainActivity";
    private static final String FILE_PREFIX = "stt";
    private static final String FILE_SUFFIX = ".txt";
    private Button recordButton;
    private Switch azureSwitch;
    private TextView speechOutput;
    private Switch saveSwitch;
    private static final int WRITE_TO_FILE = 1;
    private static final int VOICE_RECOGNITION_CODE = 100;
    private static final URI SERVICE_HOST = URI.create("ws://localhost:5000");


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        recordButton = (Button) findViewById(R.id.recordVoiceBtn);
        speechOutput = (TextView) findViewById(R.id.textOutput);
        saveSwitch = (Switch) findViewById(R.id.saveTextSwitch);
        azureSwitch = (Switch) findViewById(R.id.azureSwitch);

        String initialButtonText = "Click and Start Talking";
        recordButton.setText(initialButtonText);//

        if(!isRecordPermissionGranted())
        {
            requestRecordPermission();
        }

        recordButton.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                if(azureSwitch.isChecked())
                {
                    //run speech to text through azure service
                    SpeechConfig configSpeech = SpeechConfig.fromHost(SERVICE_HOST);
                    com.microsoft.cognitiveservices.speech.SpeechRecognizer azureRecognizer =
                            new com.microsoft.cognitiveservices.speech.SpeechRecognizer(configSpeech);
                    Future<SpeechRecognitionResult> azureFuture = azureRecognizer.recognizeOnceAsync();

                    //String waitMessage = "Please wait for the speech to be processed";
                    //Toast.makeText(
                    //        getBaseContext(), waitMessage, Toast.LENGTH_SHORT).show();

                    while(!azureFuture.isDone())
                    {
                        Handler handler = new Handler();
                        handler.postDelayed(new Runnable() {
                            public void run() {
                                //String waitMessage = "Please wait for the speech to be processed";
                                //Toast.makeText(
                                //        getApplicationContext(), waitMessage, Toast.LENGTH_SHORT).show();
                            }
                        }, 2000);
                    }

                    SpeechRecognitionResult azureResult;
                    try {
                        azureResult = azureFuture.get();
                        if(azureResult.getReason() == ResultReason.RecognizedSpeech)
                        {
                            speechOutput.setText(azureResult.getText());
                            Message msg = Message.obtain();
                            msg.what = WRITE_TO_FILE;
                            msg.obj = azureResult.getText();
                            returnMsgHandler.sendMessage(msg);

                        }
                        else if(azureResult.getReason() == ResultReason.NoMatch)
                        {
                            String noMatchMessage = "No Speech Recognized";
                            Toast.makeText(getApplicationContext(), noMatchMessage, Toast.LENGTH_SHORT).show();
                        }
                        else if(azureResult.getReason() == ResultReason.Canceled)
                        {
                            CancellationDetails cancelDetails = CancellationDetails.fromResult(azureResult);

                            Log.w(TAG, String.valueOf(cancelDetails.getReason()));
                        }
                    } catch (ExecutionException | InterruptedException e) {
                        Log.w(TAG, e);
                    }


                }
                else{
                    Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
                    intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                            RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
                    intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault());
                    intent.putExtra(RecognizerIntent.EXTRA_PROMPT, "Speak");
                    try {
                        startActivityForResult(intent, VOICE_RECOGNITION_CODE);


                    } catch (ActivityNotFoundException e) {
                        Toast.makeText(getApplicationContext(), "Device Not Supported",
                                Toast.LENGTH_SHORT).show();
                    }
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


    Handler returnMsgHandler = new Handler(new Handler.Callback() {
        public boolean handleMessage(Message msg) {
            if(msg.what == WRITE_TO_FILE)
            {
                if(saveSwitch.isChecked())
                {
                    try {
                        File resultsFile = File.createTempFile(FILE_PREFIX, FILE_SUFFIX, getExternalFilesDir(null));
                        FileOutputStream outputStream = new FileOutputStream(resultsFile, true);
                        outputStream.write(msg.obj.toString().getBytes());
                        outputStream.flush();
                        outputStream.close();

                    } catch (IOException e) {
                        Log.w(TAG, e);
                    }


                }
            }
            return false;
        }
    });

    private boolean isRecordPermissionGranted() {
        return (ActivityCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) ==
                PackageManager.PERMISSION_GRANTED);
    }

    private void requestRecordPermission(){
        ActivityCompat.requestPermissions(
                this, new String[]{Manifest.permission.RECORD_AUDIO}, 0);
    }

}
