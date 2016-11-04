package com.feeder.audacity.feeder;

import android.content.Intent;
import android.os.AsyncTask;
import android.util.Log;
import android.webkit.CookieManager;
import android.widget.Toast;

import com.google.gson.Gson;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

import static android.content.Context.MODE_PRIVATE;

/**
 * Created by sourabh on 5/11/16.
 */

public class GetData extends AsyncTask<Void, Void, Boolean> {

    private int status;

    HomeActivity context;

    GetData(final HomeActivity context) {
        this.context = context;
    }

    @Override
    protected Boolean doInBackground(Void... params) {
        try {

            URL obj2 = new URL(Constants.API);
            HttpURLConnection con = (HttpURLConnection) obj2.openConnection();
//            String cookie = context.getSharedPreferences("cookie.dat",MODE_PRIVATE).getString("cookie",null);
            CookieManager cookieManager = CookieManager.getInstance();
            String cookie =  cookieManager.getCookie(Constants.DOMAIN);
            con.setRequestMethod("GET");con.setRequestProperty("Cookie", cookie);
//            Gson gson = new Gson();
            BufferedReader in = new BufferedReader(
                    new InputStreamReader(con.getInputStream()));
            String inputLine;
            StringBuffer response = new StringBuffer();

            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
            in.close();
            cookieManager.setCookie(Constants.DOMAIN, con.getHeaderField("Set-Cookie"));
            Log.d("Json", String.valueOf(response));
            Log.d("Response cookie", con.getHeaderField("set-cookie"));
        } catch (IOException e) {
            e.printStackTrace();
        }
        return true;
    }

    @Override
    protected void onPostExecute(final Boolean success) {

    }

    @Override
    protected void onCancelled() {

    }
}