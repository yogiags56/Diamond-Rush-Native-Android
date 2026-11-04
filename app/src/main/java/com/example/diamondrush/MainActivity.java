package com.example.diamondrush;

import android.app.Activity;
import android.os.Bundle;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.example.diamondrush.ui.DiamondRushTheme;
import com.example.diamondrush.ui.TouchHudView;

/** Android-native menu and interactive gameplay visual prototype. */
public final class MainActivity extends Activity {
    private View menuView;
    private FrameLayout gameplayRoot;
    private GameplayPreviewView preview;

    private int dp(float value) {
        return (int) (value * getResources().getDisplayMetrics().density + 0.5f);
    }

    @Override
    protected void onCreate(Bundle state) {
        super.onCreate(state);
        getWindow().getDecorView().setSystemUiVisibility(
                View.SYSTEM_UI_FLAG_FULLSCREEN
                | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                | View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION);
        showMenu();
    }

    private void showMenu() {
        menuView = buildMenu();
        setContentView(menuView);
    }

    private View buildMenu() {
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setGravity(Gravity.CENTER);
        root.setPadding(dp(24), dp(20), dp(24), dp(20));
        GradientDrawable backdrop = new GradientDrawable(
                GradientDrawable.Orientation.TL_BR,
                new int[]{DiamondRushTheme.STONE_DARK, 0xff34291e, 0xff171512});
        root.setBackground(backdrop);

        ImageView gemMark = new ImageView(this);
        gemMark.setImageResource(R.drawable.diamond_rush_gem);
        gemMark.setScaleType(ImageView.ScaleType.FIT_CENTER);
        LinearLayout.LayoutParams gemParams = new LinearLayout.LayoutParams(dp(54), dp(54));
        gemParams.bottomMargin = dp(8);
        root.addView(gemMark, gemParams);

        TextView eyebrow = new TextView(this);
        eyebrow.setText("A CLASSIC ADVENTURE");
        eyebrow.setTextColor(DiamondRushTheme.GOLD_BRIGHT);
        eyebrow.setTextSize(11);
        eyebrow.setLetterSpacing(0.22f);
        eyebrow.setGravity(Gravity.CENTER);
        root.addView(eyebrow, matchWrap());

        TextView title = new TextView(this);
        title.setText("DIAMOND\nRUSH");
        title.setTextColor(DiamondRushTheme.TEXT_PRIMARY);
        title.setTextSize(38);
        title.setTypeface(Typeface.create("serif", Typeface.BOLD));
        title.setGravity(Gravity.CENTER);
        title.setShadowLayer(dp(5), 0, dp(2), 0xff000000);
        LinearLayout.LayoutParams titleParams = matchWrap();
        titleParams.topMargin = dp(8);
        titleParams.bottomMargin = dp(24);
        root.addView(title, titleParams);

        addMenuButton(root, "PLAY", v -> showGameplay());
        addMenuButton(root, "LEVEL SELECT", v ->
                Toast.makeText(this, "Data level asli belum terhubung.", Toast.LENGTH_SHORT).show());
        addMenuButton(root, "SETTINGS", v ->
                Toast.makeText(this, "Pengaturan akan ditambahkan.", Toast.LENGTH_SHORT).show());
        addMenuButton(root, "ABOUT", v ->
                Toast.makeText(this, "Diamond Rush · Native Android prototype", Toast.LENGTH_SHORT).show());

        TextView footer = new TextView(this);
        footer.setText("ANDROID EDITION  •  PROTOTYPE");
        footer.setTextColor(DiamondRushTheme.TEXT_MUTED);
        footer.setTextSize(10);
        footer.setLetterSpacing(0.12f);
        footer.setGravity(Gravity.CENTER);
        LinearLayout.LayoutParams footerParams = matchWrap();
        footerParams.topMargin = dp(22);
        root.addView(footer, footerParams);
        return root;
    }

    private void addMenuButton(LinearLayout root, String label, View.OnClickListener listener) {
        Button button = new Button(this);
        button.setText(label);
        button.setTextColor(DiamondRushTheme.TEXT_PRIMARY);
        button.setTextSize(14);
        button.setTypeface(Typeface.create("sans-serif-medium", Typeface.BOLD));
        button.setAllCaps(false);
        button.setLetterSpacing(0.08f);
        button.setBackground(buttonBackground());
        button.setPadding(dp(18), 0, dp(18), 0);
        button.setOnClickListener(listener);
        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(
                Math.min(getResources().getDisplayMetrics().widthPixels - dp(48), dp(360)),
                dp(54));
        params.topMargin = dp(7);
        params.bottomMargin = dp(7);
        root.addView(button, params);
    }

    private void showGameplay() {
        gameplayRoot = new FrameLayout(this);
        preview = new GameplayPreviewView(this);
        gameplayRoot.addView(preview, new FrameLayout.LayoutParams(
                FrameLayout.LayoutParams.MATCH_PARENT, FrameLayout.LayoutParams.MATCH_PARENT));

        TouchHudView hud = new TouchHudView(this);
        hud.setListener((control, pressed) -> {
            if (control == 6 && pressed) {
                preview.togglePause();
            } else {
                preview.onControlChanged(control, pressed);
            }
        });
        gameplayRoot.addView(hud, new FrameLayout.LayoutParams(
                FrameLayout.LayoutParams.MATCH_PARENT, FrameLayout.LayoutParams.MATCH_PARENT));

        TextView back = new TextView(this);
        back.setText("‹ MENU");
        back.setTextColor(0xffffe5b0);
        back.setTextSize(13);
        back.setGravity(Gravity.CENTER);
        back.setPadding(dp(14), dp(8), dp(14), dp(8));
        GradientDrawable backBg = new GradientDrawable();
        backBg.setColor(0xaa30271f);
        backBg.setCornerRadius(dp(10));
        backBg.setStroke(dp(1), 0xffd6a84b);
        back.setBackground(backBg);
        back.setOnClickListener(v -> showMenu());
        FrameLayout.LayoutParams backParams = new FrameLayout.LayoutParams(
                FrameLayout.LayoutParams.WRAP_CONTENT, FrameLayout.LayoutParams.WRAP_CONTENT,
                Gravity.TOP | Gravity.LEFT);
        backParams.leftMargin = dp(16);
        backParams.topMargin = dp(16);
        gameplayRoot.addView(back, backParams);
        setContentView(gameplayRoot);
    }

    @Override public void onBackPressed() {
        if (gameplayRoot != null && getWindow().getDecorView().findViewById(android.R.id.content) != null) {
            showMenu();
        } else {
            super.onBackPressed();
        }
    }

    private GradientDrawable buttonBackground() {
        GradientDrawable shape = new GradientDrawable();
        shape.setColor(DiamondRushTheme.STONE);
        shape.setCornerRadius(dp(12));
        shape.setStroke(dp(1.5f), DiamondRushTheme.GOLD);
        return shape;
    }

    private LinearLayout.LayoutParams matchWrap() {
        return new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT);
    }
}
