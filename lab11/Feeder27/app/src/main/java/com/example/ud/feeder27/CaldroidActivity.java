package com.example.ud.feeder27;

import android.icu.util.Calendar;
import android.os.Build;
import android.support.annotation.RequiresApi;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

import com.roomorama.caldroid.CaldroidFragment;

public class CaldroidActivity extends AppCompatActivity {

    @RequiresApi(api = Build.VERSION_CODES.N)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_caldroid);

        CaldroidFragment caldroidFragment = new CaldroidFragment();
        //Bundle args = new Bundle();
        //Calendar cal = Calendar.getInstance();
        //args.putInt(CaldroidFragment.MONTH, cal.get(Calendar.MONTH) + 1);
        //args.putInt(CaldroidFragment.YEAR, cal.get(Calendar.YEAR));
        //caldroidFragment.setArguments(args);
        android.support.v4.app.FragmentTransaction t = getSupportFragmentManager().beginTransaction();
        t.replace(R.id.activity_caldroid, caldroidFragment);
        t.commit();
    }
}
