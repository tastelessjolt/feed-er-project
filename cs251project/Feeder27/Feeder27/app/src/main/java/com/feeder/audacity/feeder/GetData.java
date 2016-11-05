package com.feeder.audacity.feeder;

import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.drawable.ColorDrawable;
import android.graphics.drawable.Drawable;
import android.icu.text.DateFormat;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import android.os.AsyncTask;
import android.util.Log;
import android.webkit.CookieManager;
import android.widget.Toast;

import com.google.gson.Gson;
import com.google.gson.JsonArray;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Date;
import java.util.HashMap;

import static android.content.ContentValues.TAG;
import static android.content.Context.MODE_PRIVATE;

/**
 * Created by sourabh on 5/11/16.
 */

public class GetData extends AsyncTask<Void, Void, Boolean> {

    private int status;
    private SharedPreferences cookieData;
    private SharedPreferences.Editor editor;
    public JSONArray jsonData;
    OnTaskFinishedListener mListener;
    String message = null;
    HomeActivity context;

    GetData(String message,final HomeActivity context) {
        this.context = context;
        this.message = message;
    }

    @Override
    protected Boolean doInBackground(Void... params) {
        try {
            cookieData = context.getSharedPreferences("cookie.dat",MODE_PRIVATE);
            URL obj2 = new URL(Constants.API);
            HttpURLConnection con = (HttpURLConnection) obj2.openConnection();
//            String cookie = context.getSharedPreferences("cookie.dat",MODE_PRIVATE).getString("cookie",null);
            String cookie = cookieData.getString("cookie",null);
            Log.d("my cookie", cookie);


            String query = "q=" + message;
            con.setRequestMethod("POST");
            con.setRequestProperty("Cookie", cookie);
            DataOutputStream wr = new DataOutputStream(con.getOutputStream());
            wr.writeBytes(query);
            wr.flush();
            wr.close();
//            Gson gson = new Gson();
            BufferedReader in = new BufferedReader(
                    new InputStreamReader(con.getInputStream()));
            String inputLine;
            StringBuffer response = new StringBuffer();

            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
            in.close();
            Log.d("Json", String.valueOf(response));
            Log.d("Response cookie", con.getHeaderField("set-cookie"));
            editor = cookieData.edit();
            editor.putString("cookie",con.getHeaderField("set-cookie") );
            editor.commit();
            jsonData = new JSONArray(response.toString());
        } catch (IOException | JSONException e) {
            e.printStackTrace();
        }
        return true;
    }

    @Override
    protected void onPostExecute(final Boolean success) {
        context.onBackgroundTaskCompleted(message,jsonData);
//        context.jsonData = jsonData;
//        HashMap<Date, Drawable> feedbacks = new HashMap<>();
//        for(int i=0; i < jsonData.length(); i++){
//            try {
//                JSONObject jsonObject = jsonData.getJSONObject(i);
//                SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'");
//                Date date = formatter.parse(jsonObject.getJSONObject("fields").optString("deadline") );
//                feedbacks.put(date, new ColorDrawable(jsonObject.getJSONObject("fields").optInt("course")));
//                context.caldroidFragment.setBackgroundDrawableForDates(feedbacks);
//            } catch (JSONException | ParseException e) {
//                e.printStackTrace();
//            }
//        }



    }


    public interface OnTaskFinishedListener {
        public void onFinished();
    }

    public void setOnTaskFinishedListener(OnTaskFinishedListener listener) {
        mListener = listener;
    }



    @Override
    protected void onCancelled() {

    }
}