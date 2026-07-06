#!/usr/bin/env bash
# =============================================================================
#  App Factory Generator - Android Portfolio Edition
#
#  Generates 20 subscription-first Android (Kotlin / Jetpack Compose) app
#  projects targeting high-ARPU professional micro-niches ("low download,
#  high income"). Every project follows clean architecture:
#
#    app/src/main/java/com/appfactory/<app>/
#      presentation/   (Compose UI: niche screen, paywall, theme)
#      domain/         (models + niche calculation use case)
#      data/           (Google Play Billing Library 7 wrapper)
#
#  Output root:  <Desktop>/App_Factory_Output/Android_Apps/App_NN_Name
#
#  Runs unattended on: Git Bash (Windows), WSL, Linux, macOS.
#  Requires only: bash, coreutils, sed. No network access needed.
#
#  Usage:  bash generate_app_factory.sh
# =============================================================================
set -euo pipefail

# --- Locate the Desktop across platforms -------------------------------------
detect_desktop() {
  if [ -n "${USERPROFILE:-}" ] && command -v cygpath >/dev/null 2>&1; then
    # Git Bash / MSYS2 on Windows
    echo "$(cygpath -u "$USERPROFILE")/Desktop"
  elif command -v wslpath >/dev/null 2>&1 && command -v cmd.exe >/dev/null 2>&1; then
    # WSL
    local wp
    wp="$( (cd /mnt/c 2>/dev/null && cmd.exe /c 'echo %USERPROFILE%' 2>/dev/null || true) | tr -d '\r' )"
    if [ -n "$wp" ]; then
      echo "$(wslpath -u "$wp")/Desktop"
    else
      echo "$HOME/Desktop"
    fi
  else
    # Linux / macOS
    echo "$HOME/Desktop"
  fi
}

DESKTOP="$(detect_desktop)"
OUT="$DESKTOP/App_Factory_Output"
ANDROID_ROOT="$OUT/Android_Apps"
mkdir -p "$ANDROID_ROOT"

echo "=============================================="
echo " App Factory Generator - Android Edition"
echo " Output root: $OUT"
echo "=============================================="

# --- Token substitution -------------------------------------------------------
# Template files are written with __TOKEN__ placeholders and then rewritten
# in place. Values must not contain the characters | & or backslash.
subst() {
  local f="$1"
  sed -e "s|__PKG__|${PKG}|g" \
      -e "s|__APP_NAME__|${APP_NAME}|g" \
      -e "s|__DISPLAY__|${DISPLAY}|g" \
      -e "s|__TAGLINE__|${TAGLINE}|g" \
      -e "s|__BRAND__|${BRAND}|g" \
      -e "s|__PRICE_M__|${PRICE_M}|g" \
      -e "s|__PRICE_A__|${PRICE_A}|g" \
      -e "s|__F1__|${F1}|g" \
      -e "s|__F2__|${F2}|g" \
      -e "s|__F3__|${F3}|g" \
      -e "s|__F4__|${F4}|g" \
      "$f" > "$f.tmp" && mv "$f.tmp" "$f"
}

# --- Project scaffold ----------------------------------------------------------
# Uses the per-app variables set by each app block:
#   APP_NUM APP_NAME PKG DISPLAY TAGLINE BRAND PRICE_M PRICE_A F1 F2 F3 F4
# Exports APP_DIR and JAVA_DIR for the app block to write its unique use case.
scaffold_app() {
  APP_DIR="$ANDROID_ROOT/App_${APP_NUM}_${APP_NAME}"
  SRC_DIR="$APP_DIR/app/src/main"
  JAVA_DIR="$SRC_DIR/java/com/appfactory/${PKG}"

  mkdir -p \
    "$JAVA_DIR/presentation/theme" \
    "$JAVA_DIR/presentation/niche" \
    "$JAVA_DIR/presentation/paywall" \
    "$JAVA_DIR/domain/model" \
    "$JAVA_DIR/domain/usecase" \
    "$JAVA_DIR/data/billing" \
    "$SRC_DIR/res/values" \
    "$APP_DIR/gradle/wrapper"

  # --- settings.gradle.kts ---
  cat > "$APP_DIR/settings.gradle.kts" << 'TPL'
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "__APP_NAME__"
include(":app")
TPL

  # --- root build.gradle.kts ---
  cat > "$APP_DIR/build.gradle.kts" << 'TPL'
plugins {
    id("com.android.application") version "8.5.2" apply false
    id("org.jetbrains.kotlin.android") version "2.0.20" apply false
    id("org.jetbrains.kotlin.plugin.compose") version "2.0.20" apply false
}
TPL

  # --- gradle.properties ---
  cat > "$APP_DIR/gradle.properties" << 'TPL'
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
android.nonTransitiveRClass=true
kotlin.code.style=official
TPL

  # --- gradle wrapper properties (Android Studio downloads Gradle on sync) ---
  cat > "$APP_DIR/gradle/wrapper/gradle-wrapper.properties" << 'TPL'
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\://services.gradle.org/distributions/gradle-8.9-bin.zip
networkTimeout=10000
validateDistributionUrl=true
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
TPL

  # --- app/build.gradle.kts ---
  cat > "$APP_DIR/app/build.gradle.kts" << 'TPL'
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.plugin.compose")
}

android {
    namespace = "com.appfactory.__PKG__"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.appfactory.__PKG__"
        minSdk = 26
        targetSdk = 35
        versionCode = 1
        versionName = "1.0.0"
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }
    buildFeatures {
        compose = true
    }
}

dependencies {
    val composeBom = platform("androidx.compose:compose-bom:2024.09.03")
    implementation(composeBom)
    implementation("androidx.activity:activity-compose:1.9.2")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.8.6")
    implementation("com.android.billingclient:billing-ktx:7.1.1")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.8.1")
}
TPL

  # --- proguard rules ---
  cat > "$APP_DIR/app/proguard-rules.pro" << 'TPL'
# Google Play Billing
-keep class com.android.vending.billing.** { *; }
# Keep the domain layer intact so calculation results are never stripped
-keep class com.appfactory.__PKG__.domain.** { *; }
TPL

  # --- AndroidManifest.xml ---
  cat > "$SRC_DIR/AndroidManifest.xml" << 'TPL'
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <uses-permission android:name="com.android.vending.BILLING" />

    <application
        android:allowBackup="true"
        android:label="@string/app_name"
        android:supportsRtl="true"
        android:theme="@style/Theme.__APP_NAME__">
        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>

</manifest>
TPL

  # --- res/values/themes.xml ---
  cat > "$SRC_DIR/res/values/themes.xml" << 'TPL'
<resources>
    <style name="Theme.__APP_NAME__" parent="android:Theme.Material.Light.NoActionBar" />
</resources>
TPL

  # --- res/values/strings.xml ---
  cat > "$SRC_DIR/res/values/strings.xml" << 'TPL'
<resources>
    <string name="app_name">__DISPLAY__</string>
    <string name="tagline">__TAGLINE__</string>
    <string name="paywall_title">Unlock __DISPLAY__ Premium</string>
    <string name="paywall_feature_1">__F1__</string>
    <string name="paywall_feature_2">__F2__</string>
    <string name="paywall_feature_3">__F3__</string>
    <string name="paywall_feature_4">__F4__</string>
    <string name="price_monthly_fallback">__PRICE_M__/month</string>
    <string name="price_annual_fallback">__PRICE_A__/year</string>
</resources>
TPL

  # --- presentation/theme/Theme.kt ---
  cat > "$JAVA_DIR/presentation/theme/Theme.kt" << 'TPL'
package com.appfactory.__PKG__.presentation.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val BrandColor = Color(0x__BRAND__)

private val LightColors = lightColorScheme(
    primary = BrandColor,
    secondary = BrandColor.copy(alpha = 0.8f)
)

private val DarkColors = darkColorScheme(
    primary = BrandColor.copy(alpha = 0.9f),
    secondary = BrandColor.copy(alpha = 0.7f)
)

@Composable
fun AppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    MaterialTheme(
        colorScheme = if (darkTheme) DarkColors else LightColors,
        content = content
    )
}
TPL

  # --- domain/model/CalculatorModels.kt ---
  cat > "$JAVA_DIR/domain/model/CalculatorModels.kt" << 'TPL'
package com.appfactory.__PKG__.domain.model

/** Declarative description of one input field on the niche calculator form. */
data class InputField(
    val id: String,
    val label: String,
    val suffix: String = "",
    val defaultValue: String = ""
)

/**
 * One row of calculated output. Rows flagged [isPremium] are gated behind
 * the active subscription and drive paywall conversion.
 */
data class ResultRow(
    val label: String,
    val value: String,
    val isPremium: Boolean = false
)
TPL

  # --- data/billing/BillingClientWrapper.kt ---
  cat > "$JAVA_DIR/data/billing/BillingClientWrapper.kt" << 'TPL'
package com.appfactory.__PKG__.data.billing

import android.app.Activity
import android.content.Context
import com.android.billingclient.api.AcknowledgePurchaseParams
import com.android.billingclient.api.BillingClient
import com.android.billingclient.api.BillingClientStateListener
import com.android.billingclient.api.BillingFlowParams
import com.android.billingclient.api.BillingResult
import com.android.billingclient.api.PendingPurchasesParams
import com.android.billingclient.api.ProductDetails
import com.android.billingclient.api.Purchase
import com.android.billingclient.api.PurchasesUpdatedListener
import com.android.billingclient.api.QueryProductDetailsParams
import com.android.billingclient.api.QueryPurchasesParams
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

/**
 * Data-layer wrapper around Google Play Billing Library 7.
 *
 * Exposes reactive state for the presentation layer:
 *  - [isSubscribed]: whether any active subscription entitlement exists
 *  - [products]: loaded subscription ProductDetails for the paywall
 *
 * Product IDs must match the subscription products configured in the
 * Play Console for this app's package name.
 */
class BillingClientWrapper(context: Context) : PurchasesUpdatedListener {

    companion object {
        const val MONTHLY_PRODUCT_ID = "pro_monthly"
        const val ANNUAL_PRODUCT_ID = "pro_annual"
    }

    private val _isSubscribed = MutableStateFlow(false)
    val isSubscribed: StateFlow<Boolean> = _isSubscribed.asStateFlow()

    private val _products = MutableStateFlow<List<ProductDetails>>(emptyList())
    val products: StateFlow<List<ProductDetails>> = _products.asStateFlow()

    private val billingClient = BillingClient.newBuilder(context)
        .setListener(this)
        .enablePendingPurchases(
            PendingPurchasesParams.newBuilder().enableOneTimeProducts().build()
        )
        .build()

    fun connect() {
        billingClient.startConnection(object : BillingClientStateListener {
            override fun onBillingSetupFinished(result: BillingResult) {
                if (result.responseCode == BillingClient.BillingResponseCode.OK) {
                    queryProducts()
                    refreshEntitlement()
                }
            }

            override fun onBillingServiceDisconnected() {
                // Play services will reconnect on the next user-driven action.
            }
        })
    }

    private fun queryProducts() {
        val productList = listOf(MONTHLY_PRODUCT_ID, ANNUAL_PRODUCT_ID).map { id ->
            QueryProductDetailsParams.Product.newBuilder()
                .setProductId(id)
                .setProductType(BillingClient.ProductType.SUBS)
                .build()
        }
        val params = QueryProductDetailsParams.newBuilder()
            .setProductList(productList)
            .build()
        billingClient.queryProductDetailsAsync(params) { result, detailsList ->
            if (result.responseCode == BillingClient.BillingResponseCode.OK) {
                _products.value = detailsList
            }
        }
    }

    fun refreshEntitlement() {
        val params = QueryPurchasesParams.newBuilder()
            .setProductType(BillingClient.ProductType.SUBS)
            .build()
        billingClient.queryPurchasesAsync(params) { result, purchases ->
            if (result.responseCode == BillingClient.BillingResponseCode.OK) {
                _isSubscribed.value = purchases.any {
                    it.purchaseState == Purchase.PurchaseState.PURCHASED
                }
                purchases.filter { !it.isAcknowledged }.forEach { acknowledge(it) }
            }
        }
    }

    fun launchPurchase(activity: Activity, product: ProductDetails) {
        val offerToken = product.subscriptionOfferDetails?.firstOrNull()?.offerToken ?: return
        val flowParams = BillingFlowParams.newBuilder()
            .setProductDetailsParamsList(
                listOf(
                    BillingFlowParams.ProductDetailsParams.newBuilder()
                        .setProductDetails(product)
                        .setOfferToken(offerToken)
                        .build()
                )
            )
            .build()
        billingClient.launchBillingFlow(activity, flowParams)
    }

    override fun onPurchasesUpdated(result: BillingResult, purchases: MutableList<Purchase>?) {
        if (result.responseCode == BillingClient.BillingResponseCode.OK && purchases != null) {
            purchases.forEach { purchase ->
                if (purchase.purchaseState == Purchase.PurchaseState.PURCHASED) {
                    _isSubscribed.value = true
                    if (!purchase.isAcknowledged) acknowledge(purchase)
                }
            }
        }
    }

    private fun acknowledge(purchase: Purchase) {
        val params = AcknowledgePurchaseParams.newBuilder()
            .setPurchaseToken(purchase.purchaseToken)
            .build()
        billingClient.acknowledgePurchase(params) { }
    }

    fun release() {
        billingClient.endConnection()
    }
}
TPL

  # --- presentation/paywall/PaywallScreen.kt ---
  cat > "$JAVA_DIR/presentation/paywall/PaywallScreen.kt" << 'TPL'
package com.appfactory.__PKG__.presentation.paywall

import android.app.Activity
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.AssistChip
import androidx.compose.material3.Button
import androidx.compose.material3.ElevatedCard
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import com.android.billingclient.api.ProductDetails
import com.appfactory.__PKG__.R
import com.appfactory.__PKG__.data.billing.BillingClientWrapper

/**
 * Full-screen subscription paywall. Prices come live from the Play Console
 * via ProductDetails; localized fallback strings are shown until loaded.
 */
@Composable
fun PaywallScreen(
    billing: BillingClientWrapper,
    activity: Activity,
    onDismiss: () -> Unit
) {
    val products by billing.products.collectAsState()
    val isSubscribed by billing.isSubscribed.collectAsState()
    val monthly = products.firstOrNull { it.productId == BillingClientWrapper.MONTHLY_PRODUCT_ID }
    val annual = products.firstOrNull { it.productId == BillingClientWrapper.ANNUAL_PRODUCT_ID }

    LaunchedEffect(isSubscribed) {
        if (isSubscribed) onDismiss()
    }

    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false)
    ) {
        Surface(modifier = Modifier.fillMaxSize()) {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .verticalScroll(rememberScrollState())
                    .padding(24.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.End
                ) {
                    TextButton(onClick = onDismiss) { Text("Close") }
                }
                Text(
                    text = stringResource(R.string.paywall_title),
                    style = MaterialTheme.typography.headlineMedium,
                    fontWeight = FontWeight.Bold
                )
                Text(
                    text = stringResource(R.string.tagline),
                    style = MaterialTheme.typography.bodyLarge,
                    modifier = Modifier.padding(top = 8.dp, bottom = 24.dp)
                )
                listOf(
                    stringResource(R.string.paywall_feature_1),
                    stringResource(R.string.paywall_feature_2),
                    stringResource(R.string.paywall_feature_3),
                    stringResource(R.string.paywall_feature_4)
                ).forEach { feature ->
                    Row(
                        modifier = Modifier.padding(vertical = 6.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = "+",
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.primary
                        )
                        Text(text = feature, modifier = Modifier.padding(start = 12.dp))
                    }
                }
                Spacer(Modifier.height(24.dp))
                TierCard(
                    title = "Annual",
                    price = annual?.displayPrice() ?: stringResource(R.string.price_annual_fallback),
                    badge = "BEST VALUE",
                    enabled = annual != null,
                    onClick = { annual?.let { billing.launchPurchase(activity, it) } }
                )
                Spacer(Modifier.height(12.dp))
                TierCard(
                    title = "Monthly",
                    price = monthly?.displayPrice() ?: stringResource(R.string.price_monthly_fallback),
                    badge = null,
                    enabled = monthly != null,
                    onClick = { monthly?.let { billing.launchPurchase(activity, it) } }
                )
                TextButton(
                    onClick = { billing.refreshEntitlement() },
                    modifier = Modifier
                        .align(Alignment.CenterHorizontally)
                        .padding(top = 16.dp)
                ) { Text("Restore purchases") }
                Text(
                    text = "Subscriptions renew automatically until cancelled in Google Play. " +
                        "Live prices are pulled from your Play Console configuration.",
                    style = MaterialTheme.typography.bodySmall,
                    modifier = Modifier.padding(top = 8.dp)
                )
            }
        }
    }
}

@Composable
private fun TierCard(
    title: String,
    price: String,
    badge: String?,
    enabled: Boolean,
    onClick: () -> Unit
) {
    ElevatedCard(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = title,
                    style = MaterialTheme.typography.titleLarge,
                    modifier = Modifier.weight(1f)
                )
                if (badge != null) {
                    AssistChip(onClick = {}, label = { Text(badge) })
                }
            }
            Text(
                text = price,
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.Bold,
                modifier = Modifier.padding(vertical = 8.dp)
            )
            Button(
                onClick = onClick,
                enabled = enabled,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text(if (enabled) "Subscribe" else "Loading prices...")
            }
        }
    }
}

private fun ProductDetails.displayPrice(): String? =
    subscriptionOfferDetails
        ?.firstOrNull()
        ?.pricingPhases
        ?.pricingPhaseList
        ?.firstOrNull()
        ?.formattedPrice
TPL

  # --- presentation/niche/NicheScreen.kt ---
  cat > "$JAVA_DIR/presentation/niche/NicheScreen.kt" << 'TPL'
package com.appfactory.__PKG__.presentation.niche

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.ElevatedCard
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedCard
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateMapOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import com.appfactory.__PKG__.domain.model.ResultRow
import com.appfactory.__PKG__.domain.usecase.AppSpec

/**
 * The core niche tool. Renders the input form declared by [AppSpec],
 * runs the domain-layer calculation, and gates premium result rows
 * behind the subscription entitlement.
 */
@Composable
fun NicheScreen(
    isSubscribed: Boolean,
    onUpgrade: () -> Unit,
    modifier: Modifier = Modifier
) {
    val values = remember {
        mutableStateMapOf<String, String>().apply {
            AppSpec.inputs.forEach { put(it.id, it.defaultValue) }
        }
    }
    var results by remember { mutableStateOf<List<ResultRow>>(emptyList()) }

    Column(
        modifier = modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(16.dp)
    ) {
        Text(
            text = AppSpec.title,
            style = MaterialTheme.typography.titleLarge,
            fontWeight = FontWeight.SemiBold
        )
        Text(
            text = AppSpec.description,
            style = MaterialTheme.typography.bodyMedium,
            modifier = Modifier.padding(top = 4.dp, bottom = 16.dp)
        )
        AppSpec.inputs.forEach { field ->
            OutlinedTextField(
                value = values[field.id] ?: "",
                onValueChange = { values[field.id] = it },
                label = { Text(field.label) },
                suffix = { if (field.suffix.isNotEmpty()) Text(field.suffix) },
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
                singleLine = true,
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 4.dp)
            )
        }
        Button(
            onClick = {
                val parsed = values.mapValues { it.value.toDoubleOrNull() ?: 0.0 }
                results = AppSpec.calculate(parsed)
            },
            modifier = Modifier
                .fillMaxWidth()
                .padding(vertical = 16.dp)
        ) { Text("Calculate") }

        results.forEach { row ->
            if (row.isPremium && !isSubscribed) {
                LockedResultCard(label = row.label, onUpgrade = onUpgrade)
            } else {
                ResultCard(row = row)
            }
        }
    }
}

@Composable
private fun ResultCard(row: ResultRow) {
    ElevatedCard(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp)
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = row.label,
                style = MaterialTheme.typography.bodyLarge,
                modifier = Modifier.weight(1f)
            )
            Text(
                text = row.value,
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
        }
    }
}

@Composable
private fun LockedResultCard(label: String, onUpgrade: () -> Unit) {
    OutlinedCard(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp)
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text(text = label, style = MaterialTheme.typography.bodyLarge)
                Text(
                    text = "Pro feature",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.primary
                )
            }
            TextButton(onClick = onUpgrade) { Text("Unlock") }
        }
    }
}
TPL

  # --- MainActivity.kt ---
  cat > "$JAVA_DIR/MainActivity.kt" << 'TPL'
package com.appfactory.__PKG__

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import com.appfactory.__PKG__.data.billing.BillingClientWrapper
import com.appfactory.__PKG__.presentation.niche.NicheScreen
import com.appfactory.__PKG__.presentation.paywall.PaywallScreen
import com.appfactory.__PKG__.presentation.theme.AppTheme

class MainActivity : ComponentActivity() {

    private lateinit var billing: BillingClientWrapper

    @OptIn(ExperimentalMaterial3Api::class)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        billing = BillingClientWrapper(applicationContext)
        billing.connect()
        setContent {
            AppTheme {
                val isSubscribed by billing.isSubscribed.collectAsState()
                var showPaywall by remember { mutableStateOf(false) }
                Scaffold(
                    topBar = {
                        TopAppBar(
                            title = { Text(stringResource(R.string.app_name)) },
                            actions = {
                                if (!isSubscribed) {
                                    TextButton(onClick = { showPaywall = true }) {
                                        Text("GO PRO")
                                    }
                                }
                            }
                        )
                    }
                ) { padding ->
                    NicheScreen(
                        isSubscribed = isSubscribed,
                        onUpgrade = { showPaywall = true },
                        modifier = Modifier.padding(padding)
                    )
                }
                if (showPaywall) {
                    PaywallScreen(
                        billing = billing,
                        activity = this@MainActivity,
                        onDismiss = { showPaywall = false }
                    )
                }
            }
        }
    }

    override fun onDestroy() {
        billing.release()
        super.onDestroy()
    }
}
TPL

  # Substitute tokens in every scaffolded file
  find "$APP_DIR" -type f \
    \( -name '*.kt' -o -name '*.kts' -o -name '*.xml' -o -name '*.pro' \) \
    -print0 |
  while IFS= read -r -d '' f; do
    subst "$f"
  done
}

# =============================================================================
# App 01 - FleetFuelPro : IFTA fuel tax estimator for owner-operators
# =============================================================================
APP_NUM="01"; APP_NAME="FleetFuelPro"; PKG="fleetfuelpro"
DISPLAY="Fleet Fuel Pro"
TAGLINE="IFTA quarterly fuel tax estimates for owner-operators and small fleets"
BRAND="FF1B5E20"; PRICE_M='$14.99'; PRICE_A='$119.99'
F1="Unlimited jurisdiction calculations"
F2="Net taxable gallons and tax due breakdowns"
F3="Quarterly filing summaries"
F4="Priority support for fleet accounts"
scaffold_app
cat > "$JAVA_DIR/domain/usecase/NicheUseCase.kt" << 'KOTLIN'
package com.appfactory.__PKG__.domain.usecase

import com.appfactory.__PKG__.domain.model.InputField
import com.appfactory.__PKG__.domain.model.ResultRow
import kotlin.math.abs

/**
 * IFTA jurisdiction estimator. Taxable gallons for a jurisdiction are the
 * miles driven there divided by fleet-average MPG; net gallons subtract
 * fuel actually purchased (and taxed at the pump) in that jurisdiction.
 */
object AppSpec {
    val title = "IFTA Quarterly Estimator"
    val description = "Estimate net taxable gallons and fuel tax due for a " +
        "jurisdiction based on your fleet-average fuel economy."
    val inputs = listOf(
        InputField("total_miles", "Total fleet miles (all jurisdictions)", "mi", "86500"),
        InputField("total_gallons", "Total fuel purchased (all jurisdictions)", "gal", "12400"),
        InputField("juris_miles", "Miles in this jurisdiction", "mi", "14200"),
        InputField("juris_gallons", "Fuel purchased in this jurisdiction", "gal", "1650"),
        InputField("tax_rate", "Jurisdiction tax rate", "USD/gal", "0.55")
    )

    fun calculate(v: Map<String, Double>): List<ResultRow> {
        val totalGallons = v.value("total_gallons").coerceAtLeast(0.001)
        val mpg = v.value("total_miles") / totalGallons
        val taxableGallons = if (mpg > 0.0) v.value("juris_miles") / mpg else 0.0
        val netGallons = taxableGallons - v.value("juris_gallons")
        val taxDue = netGallons * v.value("tax_rate")
        return listOf(
            ResultRow("Fleet average MPG", mpg.fmt()),
            ResultRow("Taxable gallons in jurisdiction", taxableGallons.fmt()),
            ResultRow("Net taxable gallons", netGallons.fmt(), isPremium = true),
            ResultRow(
                if (taxDue >= 0.0) "Estimated tax due" else "Estimated tax credit",
                "USD " + abs(taxDue).fmt(),
                isPremium = true
            )
        )
    }
}

private fun Map<String, Double>.value(id: String): Double = this[id] ?: 0.0
private fun Double.fmt(digits: Int = 2): String = "%,.${digits}f".format(this)
KOTLIN
subst "$JAVA_DIR/domain/usecase/NicheUseCase.kt"
echo "  [OK] App_${APP_NUM}_${APP_NAME}"

# =============================================================================
# App 02 - CraneLiftPlanner : rigging sling tension and WLL checker
# =============================================================================
APP_NUM="02"; APP_NAME="CraneLiftPlanner"; PKG="craneliftplanner"
DISPLAY="Crane Lift Planner"
TAGLINE="Sling tension and working load limit checks for riggers and lift directors"
BRAND="FFB71C1C"; PRICE_M='$19.99'; PRICE_A='$159.99'
F1="Unlimited lift plans"
F2="Sling utilization and safety verdicts"
F3="Minimum safe angle solver"
F4="Field-ready results without signal"
scaffold_app
cat > "$JAVA_DIR/domain/usecase/NicheUseCase.kt" << 'KOTLIN'
package com.appfactory.__PKG__.domain.usecase

import com.appfactory.__PKG__.domain.model.InputField
import com.appfactory.__PKG__.domain.model.ResultRow
import kotlin.math.asin
import kotlin.math.sin

/**
 * Sling tension planner. Tension per leg = W / (n * sin(angle)), where the
 * angle is measured from horizontal. Also solves the minimum sling angle
 * at which each leg stays within its working load limit.
 */
object AppSpec {
    val title = "Sling Tension Calculator"
    val description = "Check sling leg tension against the working load limit " +
        "before the load leaves the ground."
    val inputs = listOf(
        InputField("load_lbs", "Load weight", "lb", "12000"),
        InputField("legs", "Number of sling legs", "", "2"),
        InputField("angle_deg", "Sling angle from horizontal", "deg", "60"),
        InputField("sling_wll", "Working load limit per leg", "lb", "8000")
    )

    fun calculate(v: Map<String, Double>): List<ResultRow> {
        val load = v.value("load_lbs")
        val legs = v.value("legs").coerceAtLeast(1.0)
        val angle = v.value("angle_deg").coerceIn(5.0, 90.0)
        val wll = v.value("sling_wll")
        val tension = load / (legs * sin(Math.toRadians(angle)))
        val utilization = if (wll > 0.0) tension / wll * 100.0 else 0.0
        val ratio = if (wll > 0.0) load / (legs * wll) else 2.0
        val minAngle = if (ratio in 0.0..1.0) Math.toDegrees(asin(ratio)) else Double.NaN
        val verdict = if (tension <= wll) "WITHIN WLL" else "OVERLOADED - add legs or increase angle"
        return listOf(
            ResultRow("Tension per leg", tension.fmt() + " lb"),
            ResultRow("Sling utilization", utilization.fmt(1) + " %"),
            ResultRow("Safety verdict", verdict, isPremium = true),
            ResultRow(
                "Minimum safe sling angle",
                if (minAngle.isNaN()) "Not achievable with this sling" else minAngle.fmt(1) + " deg",
                isPremium = true
            )
        )
    }
}

private fun Map<String, Double>.value(id: String): Double = this[id] ?: 0.0
private fun Double.fmt(digits: Int = 2): String = "%,.${digits}f".format(this)
KOTLIN
subst "$JAVA_DIR/domain/usecase/NicheUseCase.kt"
echo "  [OK] App_${APP_NUM}_${APP_NAME}"

# =============================================================================
# App 03 - LocumTrack : locum tenens contract earnings and tax set-aside
# =============================================================================
APP_NUM="03"; APP_NAME="LocumTrack"; PKG="locumtrack"
DISPLAY="Locum Track"
TAGLINE="Contract earnings, per diem, and tax set-aside for locum tenens clinicians"
BRAND="FF0D47A1"; PRICE_M='$12.99'; PRICE_A='$99.99'
F1="Unlimited contract scenarios"
F2="Tax set-aside and take-home projections"
F3="Overtime and per diem modelling"
F4="Compare offers side by side"
scaffold_app
cat > "$JAVA_DIR/domain/usecase/NicheUseCase.kt" << 'KOTLIN'
package com.appfactory.__PKG__.domain.usecase

import com.appfactory.__PKG__.domain.model.InputField
import com.appfactory.__PKG__.domain.model.ResultRow

/**
 * Locum tenens weekly earnings model: 1099 gross from base plus overtime,
 * non-taxed per diem on top, and a self-employment tax set-aside so the
 * clinician knows the real take-home before signing.
 */
object AppSpec {
    val title = "Contract Week Analyzer"
    val description = "Project gross, tax set-aside, and true take-home for a " +
        "locum tenens contract week."
    val inputs = listOf(
        InputField("rate", "Hourly rate", "USD/hr", "185"),
        InputField("hours", "Regular hours", "hr", "40"),
        InputField("ot_hours", "Overtime hours", "hr", "8"),
        InputField("ot_mult", "Overtime multiplier", "x", "1.5"),
        InputField("perdiem_days", "Per diem days", "days", "5"),
        InputField("perdiem_rate", "Per diem rate", "USD/day", "96"),
        InputField("tax_pct", "Tax set-aside", "%", "30")
    )

    fun calculate(v: Map<String, Double>): List<ResultRow> {
        val rate = v.value("rate")
        val gross = rate * v.value("hours") + rate * v.value("ot_hours") * v.value("ot_mult")
        val perDiem = v.value("perdiem_days") * v.value("perdiem_rate")
        val taxSetAside = gross * v.value("tax_pct") / 100.0
        val takeHome = gross - taxSetAside + perDiem
        val totalHours = (v.value("hours") + v.value("ot_hours")).coerceAtLeast(0.001)
        return listOf(
            ResultRow("Gross contract earnings", "USD " + gross.fmt()),
            ResultRow("Tax-free per diem", "USD " + perDiem.fmt()),
            ResultRow("Tax set-aside", "USD " + taxSetAside.fmt(), isPremium = true),
            ResultRow("Weekly take-home", "USD " + takeHome.fmt(), isPremium = true),
            ResultRow("Effective hourly (after tax)", "USD " + (takeHome / totalHours).fmt(), isPremium = true)
        )
    }
}

private fun Map<String, Double>.value(id: String): Double = this[id] ?: 0.0
private fun Double.fmt(digits: Int = 2): String = "%,.${digits}f".format(this)
KOTLIN
subst "$JAVA_DIR/domain/usecase/NicheUseCase.kt"
echo "  [OK] App_${APP_NUM}_${APP_NAME}"

# =============================================================================
# App 04 - GrainBasis : cash grain basis and hauling netback calculator
# =============================================================================
APP_NUM="04"; APP_NAME="GrainBasis"; PKG="grainbasis"
DISPLAY="Grain Basis"
TAGLINE="Basis and freight-adjusted net price so growers pick the right elevator"
BRAND="FFF57F17"; PRICE_M='$9.99'; PRICE_A='$79.99'
F1="Unlimited elevator comparisons"
F2="Freight-adjusted net price per bushel"
F3="Full load value projections"
F4="Works offline in the cab"
scaffold_app
cat > "$JAVA_DIR/domain/usecase/NicheUseCase.kt" << 'KOTLIN'
package com.appfactory.__PKG__.domain.usecase

import com.appfactory.__PKG__.domain.model.InputField
import com.appfactory.__PKG__.domain.model.ResultRow

/**
 * Grain marketing netback: basis is local cash minus the futures reference;
 * hauling cost is spread across the bushels on the load to give a true
 * net price at the farm gate.
 */
object AppSpec {
    val title = "Basis and Netback"
    val description = "Compute local basis and the freight-adjusted net price " +
        "for a load delivered to a buyer."
    val inputs = listOf(
        InputField("cash_price", "Elevator cash bid", "USD/bu", "4.35"),
        InputField("futures", "Reference futures price", "USD/bu", "4.62"),
        InputField("haul_miles", "Haul distance (one way)", "mi", "38"),
        InputField("rate_per_mile", "Trucking rate", "USD/mi", "4.50"),
        InputField("bushels", "Bushels on load", "bu", "950")
    )

    fun calculate(v: Map<String, Double>): List<ResultRow> {
        val cash = v.value("cash_price")
        val basis = cash - v.value("futures")
        val bushels = v.value("bushels").coerceAtLeast(0.001)
        val freightPerBu = v.value("haul_miles") * v.value("rate_per_mile") / bushels
        val netPrice = cash - freightPerBu
        val loadValue = netPrice * bushels
        return listOf(
            ResultRow("Local basis", (if (basis >= 0) "+" else "") + basis.fmt() + " USD/bu"),
            ResultRow("Freight cost per bushel", "USD " + freightPerBu.fmt(3)),
            ResultRow("Net price after hauling", "USD " + netPrice.fmt(3) + "/bu", isPremium = true),
            ResultRow("Net load value", "USD " + loadValue.fmt(), isPremium = true)
        )
    }
}

private fun Map<String, Double>.value(id: String): Double = this[id] ?: 0.0
private fun Double.fmt(digits: Int = 2): String = "%,.${digits}f".format(this)
KOTLIN
subst "$JAVA_DIR/domain/usecase/NicheUseCase.kt"
echo "  [OK] App_${APP_NUM}_${APP_NAME}"

# =============================================================================
# App 05 - RoofEstimatorPro : pitched roof takeoff and bid builder
# =============================================================================
APP_NUM="05"; APP_NAME="RoofEstimatorPro"; PKG="roofestimatorpro"
DISPLAY="Roof Estimator Pro"
TAGLINE="Pitch-corrected takeoffs and margin-safe bids for roofing contractors"
BRAND="FF4E342E"; PRICE_M='$24.99'; PRICE_A='$199.99'
F1="Unlimited takeoffs and bids"
F2="Margin-protected bid pricing"
F3="Gross profit visibility per job"
F4="Waste factor tuning by material"
scaffold_app
cat > "$JAVA_DIR/domain/usecase/NicheUseCase.kt" << 'KOTLIN'
package com.appfactory.__PKG__.domain.usecase

import com.appfactory.__PKG__.domain.model.InputField
import com.appfactory.__PKG__.domain.model.ResultRow
import kotlin.math.sqrt

/**
 * Roofing takeoff: footprint area is scaled by the pitch factor
 * sqrt(1 + (rise/12)^2), converted to squares with waste, then priced.
 * Bid = cost / (1 - margin) so the margin is on price, not on cost.
 */
object AppSpec {
    val title = "Takeoff and Bid Builder"
    val description = "Turn a footprint measurement into squares, direct cost, " +
        "and a margin-safe bid."
    val inputs = listOf(
        InputField("length", "Footprint length", "ft", "120"),
        InputField("width", "Footprint width", "ft", "80"),
        InputField("pitch_rise", "Pitch rise per 12", "in", "4"),
        InputField("waste_pct", "Waste factor", "%", "10"),
        InputField("mat_per_sq", "Material cost per square", "USD", "425"),
        InputField("labor_per_sq", "Labor cost per square", "USD", "275"),
        InputField("margin_pct", "Target margin on price", "%", "22")
    )

    fun calculate(v: Map<String, Double>): List<ResultRow> {
        val rise = v.value("pitch_rise")
        val pitchFactor = sqrt(1.0 + (rise / 12.0) * (rise / 12.0))
        val area = v.value("length") * v.value("width") * pitchFactor
        val squares = area / 100.0 * (1.0 + v.value("waste_pct") / 100.0)
        val directCost = squares * (v.value("mat_per_sq") + v.value("labor_per_sq"))
        val margin = (v.value("margin_pct") / 100.0).coerceIn(0.0, 0.95)
        val bid = directCost / (1.0 - margin)
        return listOf(
            ResultRow("Pitch-corrected roof area", area.fmt(0) + " sq ft"),
            ResultRow("Squares including waste", squares.fmt(1)),
            ResultRow("Direct cost", "USD " + directCost.fmt()),
            ResultRow("Bid price", "USD " + bid.fmt(), isPremium = true),
            ResultRow("Gross profit", "USD " + (bid - directCost).fmt(), isPremium = true)
        )
    }
}

private fun Map<String, Double>.value(id: String): Double = this[id] ?: 0.0
private fun Double.fmt(digits: Int = 2): String = "%,.${digits}f".format(this)
KOTLIN
subst "$JAVA_DIR/domain/usecase/NicheUseCase.kt"
echo "  [OK] App_${APP_NUM}_${APP_NAME}"

# =============================================================================
# App 06 - PoolDoseCalc : commercial pool chlorine dosing and LSI balance
# =============================================================================
APP_NUM="06"; APP_NAME="PoolDoseCalc"; PKG="pooldosecalc"
DISPLAY="Pool Dose Calc"
TAGLINE="Chlorine dosing and Langelier saturation balance for pool service pros"
BRAND="FF006064"; PRICE_M='$11.99'; PRICE_A='$89.99'
F1="Unlimited pool profiles"
F2="Langelier Saturation Index readout"
F3="Water balance verdicts"
F4="Dose history for route customers"
scaffold_app
cat > "$JAVA_DIR/domain/usecase/NicheUseCase.kt" << 'KOTLIN'
package com.appfactory.__PKG__.domain.usecase

import com.appfactory.__PKG__.domain.model.InputField
import com.appfactory.__PKG__.domain.model.ResultRow
import kotlin.math.log10

/**
 * Pool service chemistry: calcium hypochlorite (65%) dose of roughly 2 oz per
 * 10,000 gallons raises free chlorine by 1 ppm. Water balance uses the
 * industry LSI form: pH + TF + (log10(CaH) - 0.4) + log10(TA) - 12.1.
 */
object AppSpec {
    val title = "Chlorine Dose and LSI"
    val description = "Dose free chlorine to target and check the water " +
        "balance with the Langelier Saturation Index."
    val inputs = listOf(
        InputField("gallons", "Pool volume", "gal", "25000"),
        InputField("current_fc", "Current free chlorine", "ppm", "1.2"),
        InputField("target_fc", "Target free chlorine", "ppm", "3.0"),
        InputField("ph", "pH", "", "7.6"),
        InputField("temp_f", "Water temperature", "F", "84"),
        InputField("calcium", "Calcium hardness", "ppm", "310"),
        InputField("alkalinity", "Total alkalinity", "ppm", "90")
    )

    fun calculate(v: Map<String, Double>): List<ResultRow> {
        val deltaPpm = (v.value("target_fc") - v.value("current_fc")).coerceAtLeast(0.0)
        val doseOz = deltaPpm * v.value("gallons") / 10000.0 * 2.0
        val temp = v.value("temp_f")
        val tf = when {
            temp <= 32.0 -> 0.0
            temp <= 37.0 -> 0.1
            temp <= 46.0 -> 0.2
            temp <= 53.0 -> 0.3
            temp <= 60.0 -> 0.4
            temp <= 66.0 -> 0.5
            temp <= 76.0 -> 0.6
            temp <= 84.0 -> 0.7
            temp <= 94.0 -> 0.8
            else -> 0.9
        }
        val lsi = v.value("ph") + tf +
            (log10(v.value("calcium").coerceAtLeast(1.0)) - 0.4) +
            log10(v.value("alkalinity").coerceAtLeast(1.0)) - 12.1
        val verdict = when {
            lsi < -0.3 -> "CORROSIVE - raise alkalinity or pH"
            lsi > 0.3 -> "SCALE-FORMING - lower pH or calcium"
            else -> "BALANCED"
        }
        return listOf(
            ResultRow("Cal-hypo 65% dose", doseOz.fmt(1) + " oz"),
            ResultRow("Dose in pounds", (doseOz / 16.0).fmt() + " lb"),
            ResultRow("Langelier Saturation Index", lsi.fmt(), isPremium = true),
            ResultRow("Water balance verdict", verdict, isPremium = true)
        )
    }
}

private fun Map<String, Double>.value(id: String): Double = this[id] ?: 0.0
private fun Double.fmt(digits: Int = 2): String = "%,.${digits}f".format(this)
KOTLIN
subst "$JAVA_DIR/domain/usecase/NicheUseCase.kt"
echo "  [OK] App_${APP_NUM}_${APP_NAME}"

# =============================================================================
# App 07 - WellQuotePro : water well drilling cost quoting
# =============================================================================
APP_NUM="07"; APP_NAME="WellQuotePro"; PKG="wellquotepro"
DISPLAY="Well Quote Pro"
TAGLINE="Drilling, casing, and pump quotes in minutes for water well contractors"
BRAND="FF283593"; PRICE_M='$19.99'; PRICE_A='$149.99'
F1="Unlimited well quotes"
F2="Margin-protected bid totals"
F3="Cost per foot benchmarking"
F4="Quote history by customer"
scaffold_app
cat > "$JAVA_DIR/domain/usecase/NicheUseCase.kt" << 'KOTLIN'
package com.appfactory.__PKG__.domain.usecase

import com.appfactory.__PKG__.domain.model.InputField
import com.appfactory.__PKG__.domain.model.ResultRow

/**
 * Water well quote: drilling and casing are priced per foot, pump and
 * mobilization are lump sums, and the bid applies margin on price
 * (bid = cost / (1 - margin)).
 */
object AppSpec {
    val title = "Well Drilling Quote"
    val description = "Build a complete drilling quote from depth, casing, " +
        "pump, and mobilization inputs."
    val inputs = listOf(
        InputField("depth", "Borehole depth", "ft", "280"),
        InputField("per_ft", "Drilling rate", "USD/ft", "38"),
        InputField("casing_ft", "Casing length", "ft", "120"),
        InputField("casing_per_ft", "Casing rate", "USD/ft", "14"),
        InputField("pump_cost", "Pump and install", "USD", "3800"),
        InputField("mobilization", "Mobilization fee", "USD", "1200"),
        InputField("margin_pct", "Target margin on price", "%", "20")
    )

    fun calculate(v: Map<String, Double>): List<ResultRow> {
        val drilling = v.value("depth") * v.value("per_ft")
        val casing = v.value("casing_ft") * v.value("casing_per_ft")
        val subtotal = drilling + casing + v.value("pump_cost") + v.value("mobilization")
        val margin = (v.value("margin_pct") / 100.0).coerceIn(0.0, 0.95)
        val bid = subtotal / (1.0 - margin)
        val depth = v.value("depth").coerceAtLeast(0.001)
        return listOf(
            ResultRow("Drilling cost", "USD " + drilling.fmt()),
            ResultRow("Casing cost", "USD " + casing.fmt()),
            ResultRow("Direct subtotal", "USD " + subtotal.fmt()),
            ResultRow("Quoted bid", "USD " + bid.fmt(), isPremium = true),
            ResultRow("Bid per foot", "USD " + (bid / depth).fmt(), isPremium = true)
        )
    }
}

private fun Map<String, Double>.value(id: String): Double = this[id] ?: 0.0
private fun Double.fmt(digits: Int = 2): String = "%,.${digits}f".format(this)
KOTLIN
subst "$JAVA_DIR/domain/usecase/NicheUseCase.kt"
echo "  [OK] App_${APP_NUM}_${APP_NAME}"

# =============================================================================
# App 08 - HVACChargeCalc : superheat / subcooling charge diagnostics
# =============================================================================
APP_NUM="08"; APP_NAME="HVACChargeCalc"; PKG="hvacchargecalc"
DISPLAY="HVAC Charge Calc"
TAGLINE="Superheat and subcooling diagnostics for HVAC service technicians"
BRAND="FF00695C"; PRICE_M='$14.99'; PRICE_A='$119.99'
F1="Unlimited system checks"
F2="Charge diagnosis verdicts"
F3="Deviation tracking against targets"
F4="Works at the condenser with no signal"
scaffold_app
cat > "$JAVA_DIR/domain/usecase/NicheUseCase.kt" << 'KOTLIN'
package com.appfactory.__PKG__.domain.usecase

import com.appfactory.__PKG__.domain.model.InputField
import com.appfactory.__PKG__.domain.model.ResultRow
import kotlin.math.abs

/**
 * Refrigerant charge check: superheat = suction line temp - evaporator
 * saturation temp; subcooling = condenser saturation temp - liquid line
 * temp. High superheat with low subcooling suggests undercharge; the
 * inverse suggests overcharge.
 */
object AppSpec {
    val title = "Superheat / Subcooling Check"
    val description = "Enter line and saturation temperatures to verify the " +
        "refrigerant charge against manufacturer targets."
    val inputs = listOf(
        InputField("suction_temp", "Suction line temperature", "F", "52"),
        InputField("suction_sat", "Evaporator saturation temperature", "F", "40"),
        InputField("liquid_sat", "Condenser saturation temperature", "F", "105"),
        InputField("liquid_temp", "Liquid line temperature", "F", "93"),
        InputField("target_sh", "Target superheat", "F", "12"),
        InputField("target_sc", "Target subcooling", "F", "10")
    )

    fun calculate(v: Map<String, Double>): List<ResultRow> {
        val superheat = v.value("suction_temp") - v.value("suction_sat")
        val subcooling = v.value("liquid_sat") - v.value("liquid_temp")
        val dSh = superheat - v.value("target_sh")
        val dSc = subcooling - v.value("target_sc")
        val verdict = when {
            dSh > 3.0 && dSc < -3.0 -> "LIKELY UNDERCHARGED"
            dSh < -3.0 && dSc > 3.0 -> "LIKELY OVERCHARGED"
            abs(dSh) <= 3.0 && abs(dSc) <= 3.0 -> "CHARGE WITHIN RANGE"
            else -> "CHECK AIRFLOW OR METERING DEVICE"
        }
        return listOf(
            ResultRow("Superheat", superheat.fmt(1) + " F"),
            ResultRow("Subcooling", subcooling.fmt(1) + " F"),
            ResultRow("Superheat deviation", (if (dSh >= 0) "+" else "") + dSh.fmt(1) + " F", isPremium = true),
            ResultRow("Charge diagnosis", verdict, isPremium = true)
        )
    }
}

private fun Map<String, Double>.value(id: String): Double = this[id] ?: 0.0
private fun Double.fmt(digits: Int = 2): String = "%,.${digits}f".format(this)
KOTLIN
subst "$JAVA_DIR/domain/usecase/NicheUseCase.kt"
echo "  [OK] App_${APP_NUM}_${APP_NAME}"

# =============================================================================
# App 09 - StumpQuote : stump grinding quote builder
# =============================================================================
APP_NUM="09"; APP_NAME="StumpQuote"; PKG="stumpquote"
DISPLAY="Stump Quote"
TAGLINE="Per-inch stump grinding quotes with travel and volume pricing built in"
BRAND="FF33691E"; PRICE_M='$9.99'; PRICE_A='$74.99'
F1="Unlimited quotes"
F2="Volume discount automation"
F3="Crew time estimates per job"
F4="Quote totals ready to text a customer"
scaffold_app
cat > "$JAVA_DIR/domain/usecase/NicheUseCase.kt" << 'KOTLIN'
package com.appfactory.__PKG__.domain.usecase

import com.appfactory.__PKG__.domain.model.InputField
import com.appfactory.__PKG__.domain.model.ResultRow

/**
 * Stump grinding quote: industry-standard per-inch-of-diameter pricing,
 * a volume discount at three or more stumps, plus haul-away and travel.
 * Crew time assumes roughly 15 minutes per 10 inches of diameter.
 */
object AppSpec {
    val title = "Stump Grinding Quote"
    val description = "Price a stump grinding job from diameter, count, " +
        "haul-away, and travel."
    val inputs = listOf(
        InputField("diameter_in", "Average stump diameter", "in", "28"),
        InputField("count", "Number of stumps", "", "3"),
        InputField("per_inch", "Rate per inch of diameter", "USD", "5.50"),
        InputField("haul_fee", "Debris haul-away fee", "USD", "75"),
        InputField("travel_miles", "Travel distance", "mi", "18"),
        InputField("mile_rate", "Travel rate", "USD/mi", "2.50"),
        InputField("volume_disc_pct", "Discount at 3 or more stumps", "%", "10")
    )

    fun calculate(v: Map<String, Double>): List<ResultRow> {
        val count = v.value("count").coerceAtLeast(0.0)
        val base = v.value("diameter_in") * v.value("per_inch") * count
        val discount = if (count >= 3.0) base * v.value("volume_disc_pct") / 100.0 else 0.0
        val travel = v.value("travel_miles") * v.value("mile_rate")
        val total = base - discount + v.value("haul_fee") + travel
        val crewHours = v.value("diameter_in") / 10.0 * 0.25 * count
        return listOf(
            ResultRow("Grinding subtotal", "USD " + base.fmt()),
            ResultRow("Volume discount", "-USD " + discount.fmt()),
            ResultRow("Quote total", "USD " + total.fmt(), isPremium = true),
            ResultRow("Estimated crew time", crewHours.fmt(1) + " hr", isPremium = true)
        )
    }
}

private fun Map<String, Double>.value(id: String): Double = this[id] ?: 0.0
private fun Double.fmt(digits: Int = 2): String = "%,.${digits}f".format(this)
KOTLIN
subst "$JAVA_DIR/domain/usecase/NicheUseCase.kt"
echo "  [OK] App_${APP_NUM}_${APP_NAME}"

# =============================================================================
# App 10 - AgSprayCalc : sprayer tank mix and product planning
# =============================================================================
APP_NUM="10"; APP_NAME="AgSprayCalc"; PKG="agspraycalc"
DISPLAY="Ag Spray Calc"
TAGLINE="Tank mix loads and total product planning for custom applicators"
BRAND="FF827717"; PRICE_M='$12.99'; PRICE_A='$99.99'
F1="Unlimited tank mix plans"
F2="Whole-field product totals"
F3="Tank count planning per field"
F4="Label-rate quick entry"
scaffold_app
cat > "$JAVA_DIR/domain/usecase/NicheUseCase.kt" << 'KOTLIN'
package com.appfactory.__PKG__.domain.usecase

import com.appfactory.__PKG__.domain.model.InputField
import com.appfactory.__PKG__.domain.model.ResultRow
import kotlin.math.ceil

/**
 * Sprayer tank planning: acres covered per tank comes from carrier volume
 * over the application rate; product per tank follows the label rate in
 * ounces per acre (128 fl oz per gallon).
 */
object AppSpec {
    val title = "Tank Mix Planner"
    val description = "Work out acres per tank, product per load, and total " +
        "product needed for the field."
    val inputs = listOf(
        InputField("tank_gal", "Sprayer tank size", "gal", "500"),
        InputField("rate_gpa", "Carrier application rate", "gal/ac", "15"),
        InputField("product_oz_acre", "Product label rate", "oz/ac", "32"),
        InputField("field_acres", "Field size", "ac", "240")
    )

    fun calculate(v: Map<String, Double>): List<ResultRow> {
        val rate = v.value("rate_gpa").coerceAtLeast(0.001)
        val acresPerTank = v.value("tank_gal") / rate
        val productPerTankGal = acresPerTank * v.value("product_oz_acre") / 128.0
        val tanksNeeded = if (acresPerTank > 0.0) ceil(v.value("field_acres") / acresPerTank) else 0.0
        val totalProductGal = v.value("field_acres") * v.value("product_oz_acre") / 128.0
        return listOf(
            ResultRow("Acres per tank", acresPerTank.fmt(1) + " ac"),
            ResultRow("Product per tank", productPerTankGal.fmt() + " gal"),
            ResultRow("Tanks needed for field", tanksNeeded.fmt(0), isPremium = true),
            ResultRow("Total product for field", totalProductGal.fmt() + " gal", isPremium = true)
        )
    }
}

private fun Map<String, Double>.value(id: String): Double = this[id] ?: 0.0
private fun Double.fmt(digits: Int = 2): String = "%,.${digits}f".format(this)
KOTLIN
subst "$JAVA_DIR/domain/usecase/NicheUseCase.kt"
echo "  [OK] App_${APP_NUM}_${APP_NAME}"

# =============================================================================
# App 11 - TowBillPro : towing and recovery invoice builder
# =============================================================================
APP_NUM="11"; APP_NAME="TowBillPro"; PKG="towbillpro"
DISPLAY="Tow Bill Pro"
TAGLINE="Hook, mileage, storage, and winch billing for towing and recovery operators"
BRAND="FFE65100"; PRICE_M='$16.99'; PRICE_A='$129.99'
F1="Unlimited invoices"
F2="Sales tax and total automation"
F3="Storage accrual tracking"
F4="After-hours surcharge handling"
scaffold_app
cat > "$JAVA_DIR/domain/usecase/NicheUseCase.kt" << 'KOTLIN'
package com.appfactory.__PKG__.domain.usecase

import com.appfactory.__PKG__.domain.model.InputField
import com.appfactory.__PKG__.domain.model.ResultRow

/**
 * Towing invoice: hook fee plus loaded mileage, daily storage, winch time,
 * and an after-hours surcharge, with sales tax applied to the subtotal.
 */
object AppSpec {
    val title = "Tow Invoice Builder"
    val description = "Assemble a complete tow and recovery invoice from the " +
        "standard billing components."
    val inputs = listOf(
        InputField("hook_fee", "Hook fee", "USD", "95"),
        InputField("miles", "Loaded miles", "mi", "22"),
        InputField("per_mile", "Rate per loaded mile", "USD", "4.50"),
        InputField("storage_days", "Storage days", "days", "3"),
        InputField("storage_rate", "Storage rate per day", "USD", "45"),
        InputField("winch_hrs", "Winch / recovery time", "hr", "0.5"),
        InputField("winch_rate", "Winch rate per hour", "USD", "150"),
        InputField("after_hours_fee", "After-hours surcharge", "USD", "65"),
        InputField("tax_pct", "Sales tax", "%", "8.25")
    )

    fun calculate(v: Map<String, Double>): List<ResultRow> {
        val mileage = v.value("miles") * v.value("per_mile")
        val storage = v.value("storage_days") * v.value("storage_rate")
        val winch = v.value("winch_hrs") * v.value("winch_rate")
        val subtotal = v.value("hook_fee") + mileage + storage + winch + v.value("after_hours_fee")
        val tax = subtotal * v.value("tax_pct") / 100.0
        return listOf(
            ResultRow("Mileage charge", "USD " + mileage.fmt()),
            ResultRow("Storage charge", "USD " + storage.fmt()),
            ResultRow("Subtotal", "USD " + subtotal.fmt()),
            ResultRow("Sales tax", "USD " + tax.fmt(), isPremium = true),
            ResultRow("Invoice total", "USD " + (subtotal + tax).fmt(), isPremium = true)
        )
    }
}

private fun Map<String, Double>.value(id: String): Double = this[id] ?: 0.0
private fun Double.fmt(digits: Int = 2): String = "%,.${digits}f".format(this)
KOTLIN
subst "$JAVA_DIR/domain/usecase/NicheUseCase.kt"
echo "  [OK] App_${APP_NUM}_${APP_NAME}"

# =============================================================================
# App 12 - NotaryLedger : notary invoice and SE-tax split tracker
# =============================================================================
APP_NUM="12"; APP_NAME="NotaryLedger"; PKG="notaryledger"
DISPLAY="Notary Ledger"
TAGLINE="Signing invoices with the self-employment tax split notaries need at filing time"
BRAND="FF4A148C"; PRICE_M='$9.99'; PRICE_A='$79.99'
F1="Unlimited signing invoices"
F2="SE-tax-exempt fee separation"
F3="Mileage deduction tracking"
F4="Year-end totals by category"
scaffold_app
cat > "$JAVA_DIR/domain/usecase/NicheUseCase.kt" << 'KOTLIN'
package com.appfactory.__PKG__.domain.usecase

import com.appfactory.__PKG__.domain.model.InputField
import com.appfactory.__PKG__.domain.model.ResultRow

/**
 * Notary signing invoice: statutory notarial act fees are exempt from
 * self-employment tax in the US, while travel, printing, and other
 * ancillary fees are not - so the split matters at filing time.
 */
object AppSpec {
    val title = "Signing Invoice and Tax Split"
    val description = "Build a signing invoice and separate SE-tax-exempt " +
        "notarial fees from taxable ancillary income."
    val inputs = listOf(
        InputField("acts", "Notarial acts", "", "6"),
        InputField("fee_per_act", "Statutory fee per act", "USD", "15"),
        InputField("travel_fee", "Travel fee", "USD", "35"),
        InputField("pages", "Pages printed", "", "24"),
        InputField("per_page", "Printing fee per page", "USD", "0.25"),
        InputField("mileage", "Miles driven", "mi", "14"),
        InputField("mile_rate", "Mileage rate", "USD/mi", "0.67")
    )

    fun calculate(v: Map<String, Double>): List<ResultRow> {
        val notarialFees = v.value("acts") * v.value("fee_per_act")
        val ancillary = v.value("travel_fee") +
            v.value("pages") * v.value("per_page") +
            v.value("mileage") * v.value("mile_rate")
        val total = notarialFees + ancillary
        return listOf(
            ResultRow("Notarial act fees", "USD " + notarialFees.fmt()),
            ResultRow("Ancillary fees", "USD " + ancillary.fmt()),
            ResultRow("Invoice total", "USD " + total.fmt()),
            ResultRow("SE-tax-exempt portion", "USD " + notarialFees.fmt(), isPremium = true),
            ResultRow("SE-taxable portion", "USD " + ancillary.fmt(), isPremium = true)
        )
    }
}

private fun Map<String, Double>.value(id: String): Double = this[id] ?: 0.0
private fun Double.fmt(digits: Int = 2): String = "%,.${digits}f".format(this)
KOTLIN
subst "$JAVA_DIR/domain/usecase/NicheUseCase.kt"
echo "  [OK] App_${APP_NUM}_${APP_NAME}"

# =============================================================================
# App 13 - SepticSizer : septic tank and drainfield sizing
# =============================================================================
APP_NUM="13"; APP_NAME="SepticSizer"; PKG="septicsizer"
DISPLAY="Septic Sizer"
TAGLINE="Tank and drainfield sizing from bedrooms and perc rate for site evaluators"
BRAND="FF37474F"; PRICE_M='$14.99'; PRICE_A='$109.99'
F1="Unlimited site calculations"
F2="Drainfield area and trench layout"
F3="Perc-rate based application rates"
F4="Printable sizing summaries"
scaffold_app
cat > "$JAVA_DIR/domain/usecase/NicheUseCase.kt" << 'KOTLIN'
package com.appfactory.__PKG__.domain.usecase

import com.appfactory.__PKG__.domain.model.InputField
import com.appfactory.__PKG__.domain.model.ResultRow

/**
 * Conventional septic sizing: design flow at gallons per bedroom per day,
 * tank at 1.5x daily flow with a 1000 gallon floor, and a soil application
 * rate stepped down as the percolation rate slows. Always verify against
 * the local health code, which governs.
 */
object AppSpec {
    val title = "Tank and Drainfield Sizing"
    val description = "Size the tank and drainfield from bedroom count and " +
        "the measured percolation rate."
    val inputs = listOf(
        InputField("bedrooms", "Bedrooms", "", "4"),
        InputField("gpd_per_bedroom", "Design flow per bedroom", "gal/day", "150"),
        InputField("perc_rate", "Percolation rate", "min/in", "35"),
        InputField("trench_width_ft", "Trench width", "ft", "3")
    )

    fun calculate(v: Map<String, Double>): List<ResultRow> {
        val flow = v.value("bedrooms") * v.value("gpd_per_bedroom")
        val tank = (flow * 1.5).coerceAtLeast(1000.0)
        val perc = v.value("perc_rate")
        val ltar = when {
            perc <= 10.0 -> 0.9
            perc <= 30.0 -> 0.6
            perc <= 45.0 -> 0.45
            perc <= 60.0 -> 0.3
            else -> 0.2
        }
        val area = flow / ltar
        val trenchLen = area / v.value("trench_width_ft").coerceAtLeast(0.001)
        return listOf(
            ResultRow("Design flow", flow.fmt(0) + " gal/day"),
            ResultRow("Minimum tank size", tank.fmt(0) + " gal"),
            ResultRow("Soil application rate", ltar.fmt() + " gal/sqft/day"),
            ResultRow("Drainfield area", area.fmt(0) + " sq ft", isPremium = true),
            ResultRow("Total trench length", trenchLen.fmt(0) + " ft", isPremium = true)
        )
    }
}

private fun Map<String, Double>.value(id: String): Double = this[id] ?: 0.0
private fun Double.fmt(digits: Int = 2): String = "%,.${digits}f".format(this)
KOTLIN
subst "$JAVA_DIR/domain/usecase/NicheUseCase.kt"
echo "  [OK] App_${APP_NUM}_${APP_NAME}"

# =============================================================================
# App 14 - WeldCostCalc : weld metal, consumables, and arc time costing
# =============================================================================
APP_NUM="14"; APP_NAME="WeldCostCalc"; PKG="weldcostcalc"
DISPLAY="Weld Cost Calc"
TAGLINE="Consumable weight, arc time, and true cost per weld for fab shops"
BRAND="FFBF360C"; PRICE_M='$17.99'; PRICE_A='$139.99'
F1="Unlimited weld costings"
F2="Arc time and labor cost projections"
F3="Deposition efficiency tuning"
F4="Job-level cost rollups"
scaffold_app
cat > "$JAVA_DIR/domain/usecase/NicheUseCase.kt" << 'KOTLIN'
package com.appfactory.__PKG__.domain.usecase

import com.appfactory.__PKG__.domain.model.InputField
import com.appfactory.__PKG__.domain.model.ResultRow

/**
 * Fillet weld costing: deposited volume is 0.5 * leg^2 * length, steel at
 * 0.283 lb/cubic inch. Consumables scale up by deposition efficiency and
 * arc time comes from the process deposition rate in lb/hr.
 */
object AppSpec {
    val title = "Fillet Weld Costing"
    val description = "Cost a fillet weld from length and leg size through " +
        "consumables, arc time, and labor."
    val inputs = listOf(
        InputField("length_in", "Total weld length", "in", "240"),
        InputField("fillet_in", "Fillet leg size", "in", "0.25"),
        InputField("rod_price_lb", "Consumable price", "USD/lb", "4.20"),
        InputField("efficiency_pct", "Deposition efficiency", "%", "65"),
        InputField("dep_rate", "Deposition rate", "lb/hr", "3.5"),
        InputField("labor_rate", "Shop labor rate", "USD/hr", "85")
    )

    fun calculate(v: Map<String, Double>): List<ResultRow> {
        val leg = v.value("fillet_in")
        val volume = 0.5 * leg * leg * v.value("length_in")
        val depositedLb = volume * 0.283
        val efficiency = (v.value("efficiency_pct") / 100.0).coerceIn(0.01, 1.0)
        val consumableLb = depositedLb / efficiency
        val rodCost = consumableLb * v.value("rod_price_lb")
        val arcHours = depositedLb / v.value("dep_rate").coerceAtLeast(0.001)
        val laborCost = arcHours * v.value("labor_rate")
        return listOf(
            ResultRow("Deposited weld metal", depositedLb.fmt() + " lb"),
            ResultRow("Consumables required", consumableLb.fmt() + " lb"),
            ResultRow("Consumable cost", "USD " + rodCost.fmt()),
            ResultRow("Arc time", arcHours.fmt() + " hr", isPremium = true),
            ResultRow("Total weld cost", "USD " + (rodCost + laborCost).fmt(), isPremium = true)
        )
    }
}

private fun Map<String, Double>.value(id: String): Double = this[id] ?: 0.0
private fun Double.fmt(digits: Int = 2): String = "%,.${digits}f".format(this)
KOTLIN
subst "$JAVA_DIR/domain/usecase/NicheUseCase.kt"
echo "  [OK] App_${APP_NUM}_${APP_NAME}"

# =============================================================================
# App 15 - ColdChainLog : refrigerated transport compliance checker
# =============================================================================
APP_NUM="15"; APP_NAME="ColdChainLog"; PKG="coldchainlog"
DISPLAY="Cold Chain Log"
TAGLINE="Temperature excursion checks for reefer loads and food safety compliance"
BRAND="FF01579B"; PRICE_M='$21.99'; PRICE_A='$179.99'
F1="Unlimited load checks"
F2="Excursion severity readouts"
F3="Compliance verdicts per load"
F4="Audit-ready trip summaries"
scaffold_app
cat > "$JAVA_DIR/domain/usecase/NicheUseCase.kt" << 'KOTLIN'
package com.appfactory.__PKG__.domain.usecase

import com.appfactory.__PKG__.domain.model.InputField
import com.appfactory.__PKG__.domain.model.ResultRow
import kotlin.math.max

/**
 * Cold chain compliance: five checkpoint readings are compared against the
 * commodity's allowed band. Any reading outside the band is an excursion;
 * the worst deviation drives the severity readout.
 */
object AppSpec {
    val title = "Reefer Load Compliance Check"
    val description = "Enter checkpoint temperatures and the allowed band to " +
        "verify the load stayed in range."
    val inputs = listOf(
        InputField("min_f", "Minimum allowed temperature", "F", "33"),
        InputField("max_f", "Maximum allowed temperature", "F", "40"),
        InputField("r1", "Reading 1 (pickup)", "F", "36"),
        InputField("r2", "Reading 2", "F", "38"),
        InputField("r3", "Reading 3", "F", "41"),
        InputField("r4", "Reading 4", "F", "37"),
        InputField("r5", "Reading 5 (delivery)", "F", "39")
    )

    fun calculate(v: Map<String, Double>): List<ResultRow> {
        val lo = v.value("min_f")
        val hi = v.value("max_f")
        val readings = listOf(v.value("r1"), v.value("r2"), v.value("r3"), v.value("r4"), v.value("r5"))
        val excursions = readings.count { it < lo || it > hi }
        val average = readings.average()
        val maxDeviation = readings.maxOf { max(max(lo - it, it - hi), 0.0) }
        val verdict = if (excursions == 0) "COMPLIANT" else "EXCURSION - document and notify receiver"
        return listOf(
            ResultRow("Average temperature", average.fmt(1) + " F"),
            ResultRow("Readings out of range", excursions.toString() + " of " + readings.size),
            ResultRow("Worst deviation", maxDeviation.fmt(1) + " F", isPremium = true),
            ResultRow("Compliance verdict", verdict, isPremium = true)
        )
    }
}

private fun Map<String, Double>.value(id: String): Double = this[id] ?: 0.0
private fun Double.fmt(digits: Int = 2): String = "%,.${digits}f".format(this)
KOTLIN
subst "$JAVA_DIR/domain/usecase/NicheUseCase.kt"
echo "  [OK] App_${APP_NUM}_${APP_NAME}"

# =============================================================================
# App 16 - HayTradePro : hay pricing with moisture adjustment
# =============================================================================
APP_NUM="16"; APP_NAME="HayTradePro"; PKG="haytradepro"
DISPLAY="Hay Trade Pro"
TAGLINE="Moisture-adjusted price per ton so hay buyers compare lots fairly"
BRAND="FF6D4C41"; PRICE_M='$9.99'; PRICE_A='$74.99'
F1="Unlimited lot comparisons"
F2="Moisture-adjusted pricing"
F3="Dry matter value analysis"
F4="Per-bale and per-ton views"
scaffold_app
cat > "$JAVA_DIR/domain/usecase/NicheUseCase.kt" << 'KOTLIN'
package com.appfactory.__PKG__.domain.usecase

import com.appfactory.__PKG__.domain.model.InputField
import com.appfactory.__PKG__.domain.model.ResultRow

/**
 * Hay lot pricing: converts a bale price to as-fed dollars per ton, then
 * normalizes to a standard moisture basis via dry matter so a wet lot and
 * a dry lot can be compared on equal terms.
 */
object AppSpec {
    val title = "Moisture-Adjusted Hay Pricing"
    val description = "Convert a bale price to dollars per ton on a standard " +
        "moisture basis before you commit to the lot."
    val inputs = listOf(
        InputField("bale_price", "Price per bale", "USD", "85"),
        InputField("bale_lbs", "Bale weight", "lb", "1250"),
        InputField("moisture_pct", "Lot moisture", "%", "18"),
        InputField("standard_moisture", "Standard moisture basis", "%", "15")
    )

    fun calculate(v: Map<String, Double>): List<ResultRow> {
        val lbs = v.value("bale_lbs").coerceAtLeast(0.001)
        val price = v.value("bale_price")
        val asFedPerTon = price / (lbs / 2000.0)
        val moisture = (v.value("moisture_pct") / 100.0).coerceIn(0.0, 0.99)
        val standard = (v.value("standard_moisture") / 100.0).coerceIn(0.0, 0.99)
        val dryMatterLbs = lbs * (1.0 - moisture)
        val standardEquivalentLbs = dryMatterLbs / (1.0 - standard)
        val adjustedPerTon = price / (standardEquivalentLbs / 2000.0)
        return listOf(
            ResultRow("As-fed price per ton", "USD " + asFedPerTon.fmt()),
            ResultRow("Dry matter per bale", dryMatterLbs.fmt(0) + " lb"),
            ResultRow("Adjusted price per ton", "USD " + adjustedPerTon.fmt(), isPremium = true),
            ResultRow("Moisture penalty per ton", "USD " + (adjustedPerTon - asFedPerTon).fmt(), isPremium = true)
        )
    }
}

private fun Map<String, Double>.value(id: String): Double = this[id] ?: 0.0
private fun Double.fmt(digits: Int = 2): String = "%,.${digits}f".format(this)
KOTLIN
subst "$JAVA_DIR/domain/usecase/NicheUseCase.kt"
echo "  [OK] App_${APP_NUM}_${APP_NAME}"

# =============================================================================
# App 17 - FreightClassCalc : LTL density and freight class
# =============================================================================
APP_NUM="17"; APP_NAME="FreightClassCalc"; PKG="freightclasscalc"
DISPLAY="Freight Class Calc"
TAGLINE="Density-based NMFC freight class and linehaul estimates for shippers"
BRAND="FF1A237E"; PRICE_M='$18.99'; PRICE_A='$149.99'
F1="Unlimited shipment calculations"
F2="Instant NMFC class lookup"
F3="Linehaul cost estimates"
F4="Multi-pallet density rollups"
scaffold_app
cat > "$JAVA_DIR/domain/usecase/NicheUseCase.kt" << 'KOTLIN'
package com.appfactory.__PKG__.domain.usecase

import com.appfactory.__PKG__.domain.model.InputField
import com.appfactory.__PKG__.domain.model.ResultRow

/**
 * LTL freight class: density in pounds per cubic foot maps onto the
 * standard NMFC density break table; the linehaul estimate applies a
 * rate per hundredweight (cwt).
 */
object AppSpec {
    val title = "Density and Freight Class"
    val description = "Get the NMFC density class and an estimated linehaul " +
        "charge from pallet dimensions and weight."
    val inputs = listOf(
        InputField("length_in", "Length", "in", "48"),
        InputField("width_in", "Width", "in", "40"),
        InputField("height_in", "Height", "in", "60"),
        InputField("weight_lbs", "Weight", "lb", "925"),
        InputField("rate_per_cwt", "Rate per cwt", "USD", "38")
    )

    fun calculate(v: Map<String, Double>): List<ResultRow> {
        val cubicFeet = v.value("length_in") * v.value("width_in") * v.value("height_in") / 1728.0
        val density = if (cubicFeet > 0.0) v.value("weight_lbs") / cubicFeet else 0.0
        val freightClass = when {
            density >= 50.0 -> "50"
            density >= 35.0 -> "55"
            density >= 30.0 -> "60"
            density >= 22.5 -> "65"
            density >= 15.0 -> "70"
            density >= 13.5 -> "77.5"
            density >= 12.0 -> "85"
            density >= 10.5 -> "92.5"
            density >= 9.0 -> "100"
            density >= 8.0 -> "110"
            density >= 7.0 -> "125"
            density >= 6.0 -> "150"
            density >= 5.0 -> "175"
            density >= 4.0 -> "200"
            density >= 3.0 -> "250"
            density >= 2.0 -> "300"
            density >= 1.0 -> "400"
            else -> "500"
        }
        val linehaul = v.value("weight_lbs") / 100.0 * v.value("rate_per_cwt")
        return listOf(
            ResultRow("Shipment volume", cubicFeet.fmt(1) + " cu ft"),
            ResultRow("Density", density.fmt(1) + " lb/cu ft"),
            ResultRow("NMFC freight class", freightClass, isPremium = true),
            ResultRow("Estimated linehaul", "USD " + linehaul.fmt(), isPremium = true)
        )
    }
}

private fun Map<String, Double>.value(id: String): Double = this[id] ?: 0.0
private fun Double.fmt(digits: Int = 2): String = "%,.${digits}f".format(this)
KOTLIN
subst "$JAVA_DIR/domain/usecase/NicheUseCase.kt"
echo "  [OK] App_${APP_NUM}_${APP_NAME}"

# =============================================================================
# App 18 - BarPourCost : beverage pour cost and menu pricing
# =============================================================================
APP_NUM="18"; APP_NAME="BarPourCost"; PKG="barpourcost"
DISPLAY="Bar Pour Cost"
TAGLINE="Pour cost percentage and target-margin menu pricing for bar managers"
BRAND="FF880E4F"; PRICE_M='$13.99'; PRICE_A='$109.99'
F1="Unlimited bottle costings"
F2="Target pour cost pricing"
F3="Margin per pour visibility"
F4="Menu-wide pricing reviews"
scaffold_app
cat > "$JAVA_DIR/domain/usecase/NicheUseCase.kt" << 'KOTLIN'
package com.appfactory.__PKG__.domain.usecase

import com.appfactory.__PKG__.domain.model.InputField
import com.appfactory.__PKG__.domain.model.ResultRow

/**
 * Bar program math: pours per bottle from metric bottle size and the ounce
 * pour spec (29.5735 ml per fl oz), pour cost as a percentage of menu
 * price, and the menu price needed to hit a target pour cost.
 */
object AppSpec {
    val title = "Pour Cost Analyzer"
    val description = "Check the pour cost on a bottle and find the menu " +
        "price that hits your target percentage."
    val inputs = listOf(
        InputField("bottle_cost", "Bottle cost", "USD", "24"),
        InputField("bottle_ml", "Bottle size", "ml", "750"),
        InputField("pour_oz", "Pour size", "oz", "1.5"),
        InputField("menu_price", "Current menu price", "USD", "12"),
        InputField("target_pct", "Target pour cost", "%", "20")
    )

    fun calculate(v: Map<String, Double>): List<ResultRow> {
        val pourMl = (v.value("pour_oz") * 29.5735).coerceAtLeast(0.001)
        val pours = v.value("bottle_ml") / pourMl
        val costPerPour = if (pours > 0.0) v.value("bottle_cost") / pours else 0.0
        val menuPrice = v.value("menu_price").coerceAtLeast(0.001)
        val pourCostPct = costPerPour / menuPrice * 100.0
        val target = (v.value("target_pct") / 100.0).coerceAtLeast(0.001)
        val suggestedPrice = costPerPour / target
        return listOf(
            ResultRow("Pours per bottle", pours.fmt(1)),
            ResultRow("Cost per pour", "USD " + costPerPour.fmt()),
            ResultRow("Pour cost", pourCostPct.fmt(1) + " %"),
            ResultRow("Margin per pour", "USD " + (menuPrice - costPerPour).fmt(), isPremium = true),
            ResultRow("Price for target pour cost", "USD " + suggestedPrice.fmt(), isPremium = true)
        )
    }
}

private fun Map<String, Double>.value(id: String): Double = this[id] ?: 0.0
private fun Double.fmt(digits: Int = 2): String = "%,.${digits}f".format(this)
KOTLIN
subst "$JAVA_DIR/domain/usecase/NicheUseCase.kt"
echo "  [OK] App_${APP_NUM}_${APP_NAME}"

# =============================================================================
# App 19 - SolarROIPro : commercial solar payback and ROI
# =============================================================================
APP_NUM="19"; APP_NAME="SolarROIPro"; PKG="solarroipro"
DISPLAY="Solar ROI Pro"
TAGLINE="Payback and 25-year ROI numbers solar sales teams can defend"
BRAND="FFEF6C00"; PRICE_M='$29.99'; PRICE_A='$239.99'
F1="Unlimited proposals"
F2="Payback period modelling"
F3="25-year ROI projections"
F4="Incentive-adjusted system costs"
scaffold_app
cat > "$JAVA_DIR/domain/usecase/NicheUseCase.kt" << 'KOTLIN'
package com.appfactory.__PKG__.domain.usecase

import com.appfactory.__PKG__.domain.model.InputField
import com.appfactory.__PKG__.domain.model.ResultRow

/**
 * Solar proposal economics: net cost after incentives, annual production
 * from peak sun hours with a 0.8 system performance ratio, utility-rate
 * savings, simple payback, and 25-year return on the net investment.
 */
object AppSpec {
    val title = "Solar Payback and ROI"
    val description = "Model net cost, production, payback, and long-run ROI " +
        "for a proposed system."
    val inputs = listOf(
        InputField("kw", "System size", "kW", "48"),
        InputField("cost_per_watt", "Installed cost", "USD/W", "2.10"),
        InputField("incentive_pct", "Incentives and tax credit", "%", "30"),
        InputField("sun_hours", "Peak sun hours per day", "hr", "5.2"),
        InputField("rate_kwh", "Utility rate", "USD/kWh", "0.14")
    )

    fun calculate(v: Map<String, Double>): List<ResultRow> {
        val netCost = v.value("kw") * 1000.0 * v.value("cost_per_watt") *
            (1.0 - (v.value("incentive_pct") / 100.0).coerceIn(0.0, 1.0))
        val annualKwh = v.value("kw") * v.value("sun_hours") * 365.0 * 0.8
        val annualSavings = annualKwh * v.value("rate_kwh")
        val payback = if (annualSavings > 0.0) netCost / annualSavings else 0.0
        val roi25 = if (netCost > 0.0) (annualSavings * 25.0 - netCost) / netCost * 100.0 else 0.0
        return listOf(
            ResultRow("Net system cost", "USD " + netCost.fmt()),
            ResultRow("Annual production", annualKwh.fmt(0) + " kWh"),
            ResultRow("Annual savings", "USD " + annualSavings.fmt()),
            ResultRow("Simple payback", payback.fmt(1) + " years", isPremium = true),
            ResultRow("25-year ROI", roi25.fmt(0) + " %", isPremium = true)
        )
    }
}

private fun Map<String, Double>.value(id: String): Double = this[id] ?: 0.0
private fun Double.fmt(digits: Int = 2): String = "%,.${digits}f".format(this)
KOTLIN
subst "$JAVA_DIR/domain/usecase/NicheUseCase.kt"
echo "  [OK] App_${APP_NUM}_${APP_NAME}"

# =============================================================================
# App 20 - DumpsterQuote : roll-off rental quoting with overage handling
# =============================================================================
APP_NUM="20"; APP_NAME="DumpsterQuote"; PKG="dumpsterquote"
DISPLAY="Dumpster Quote"
TAGLINE="Roll-off quotes with day and tonnage overage math built in"
BRAND="FF455A64"; PRICE_M='$15.99'; PRICE_A='$124.99'
F1="Unlimited quotes"
F2="Tonnage overage automation"
F3="Extended rental pricing"
F4="Effective daily rate insights"
scaffold_app
cat > "$JAVA_DIR/domain/usecase/NicheUseCase.kt" << 'KOTLIN'
package com.appfactory.__PKG__.domain.usecase

import com.appfactory.__PKG__.domain.model.InputField
import com.appfactory.__PKG__.domain.model.ResultRow
import kotlin.math.max

/**
 * Roll-off dumpster quote: flat base rate covers an included rental period
 * and tonnage allowance; extra days and estimated tonnage overage are
 * billed on top, and the effective daily rate shows deal quality.
 */
object AppSpec {
    val title = "Roll-Off Rental Quote"
    val description = "Quote a roll-off rental including extra-day charges " +
        "and estimated tonnage overage."
    val inputs = listOf(
        InputField("base_rate", "Base rate (size and haul)", "USD", "485"),
        InputField("included_days", "Included rental days", "days", "7"),
        InputField("rental_days", "Expected rental days", "days", "12"),
        InputField("extra_day_rate", "Extra day rate", "USD/day", "15"),
        InputField("included_tons", "Included tonnage", "tons", "4"),
        InputField("est_tons", "Estimated tonnage", "tons", "5.5"),
        InputField("overage_per_ton", "Overage rate", "USD/ton", "95")
    )

    fun calculate(v: Map<String, Double>): List<ResultRow> {
        val extraDays = max(0.0, v.value("rental_days") - v.value("included_days"))
        val extraDayCharge = extraDays * v.value("extra_day_rate")
        val overageTons = max(0.0, v.value("est_tons") - v.value("included_tons"))
        val overageCharge = overageTons * v.value("overage_per_ton")
        val total = v.value("base_rate") + extraDayCharge + overageCharge
        val days = v.value("rental_days").coerceAtLeast(1.0)
        return listOf(
            ResultRow("Extra day charges", "USD " + extraDayCharge.fmt()),
            ResultRow("Tonnage overage", "USD " + overageCharge.fmt()),
            ResultRow("Quote total", "USD " + total.fmt(), isPremium = true),
            ResultRow("Effective rate per day", "USD " + (total / days).fmt(), isPremium = true)
        )
    }
}

private fun Map<String, Double>.value(id: String): Double = this[id] ?: 0.0
private fun Double.fmt(digits: Int = 2): String = "%,.${digits}f".format(this)
KOTLIN
subst "$JAVA_DIR/domain/usecase/NicheUseCase.kt"
echo "  [OK] App_${APP_NUM}_${APP_NAME}"

# =============================================================================
# Portfolio README + final summary
# =============================================================================
cat > "$OUT/README.md" << 'READMEEOF'
# App Factory Output - Android Portfolio

20 subscription-first Android apps (Kotlin / Jetpack Compose), each targeting
a high-ARPU professional micro-niche. Every project follows clean
architecture (presentation / domain / data) and ships with a working
paywall wired to Google Play Billing Library 7.

## The portfolio

| # | App | Niche |
|---|-----|-------|
| 01 | Fleet Fuel Pro | IFTA fuel tax estimation for owner-operators |
| 02 | Crane Lift Planner | Rigging sling tension and WLL checks |
| 03 | Locum Track | Locum tenens contract earnings and tax set-aside |
| 04 | Grain Basis | Cash grain basis and hauling netback |
| 05 | Roof Estimator Pro | Pitched roof takeoffs and margin-safe bids |
| 06 | Pool Dose Calc | Chlorine dosing and LSI water balance |
| 07 | Well Quote Pro | Water well drilling quotes |
| 08 | HVAC Charge Calc | Superheat / subcooling charge diagnostics |
| 09 | Stump Quote | Stump grinding quote builder |
| 10 | Ag Spray Calc | Sprayer tank mix and product planning |
| 11 | Tow Bill Pro | Towing and recovery invoicing |
| 12 | Notary Ledger | Notary invoices with SE-tax split |
| 13 | Septic Sizer | Septic tank and drainfield sizing |
| 14 | Weld Cost Calc | Weld consumable and arc time costing |
| 15 | Cold Chain Log | Reefer temperature compliance checks |
| 16 | Hay Trade Pro | Moisture-adjusted hay pricing |
| 17 | Freight Class Calc | LTL density and NMFC freight class |
| 18 | Bar Pour Cost | Beverage pour cost and menu pricing |
| 19 | Solar ROI Pro | Commercial solar payback and ROI |
| 20 | Dumpster Quote | Roll-off rental quoting with overages |

## Opening a project

1. Install Android Studio (any recent version).
2. File > Open > select one app folder (e.g. `Android_Apps/App_01_FleetFuelPro`).
3. On first sync Android Studio downloads Gradle 8.9 automatically (per
   `gradle/wrapper/gradle-wrapper.properties`) plus all dependencies.
4. Run on an emulator or device. The calculator works immediately; the
   paywall UI renders with fallback prices until Play billing is configured.

## Monetization wiring (per app, when you are ready to ship one)

1. Create the app in Play Console under its `applicationId`
   (`com.appfactory.<name>`).
2. Add two subscription products with IDs `pro_monthly` and `pro_annual`
   (these match `BillingClientWrapper.kt`), each with one base plan.
3. Upload a signed internal-testing build; live prices then flow into the
   paywall automatically via ProductDetails.

## What is deliberately NOT included

Launcher icons, store listings, privacy policies, signing keys, and deep
feature sets. These scaffolds are starting points: pick the strongest
niches and build them out into genuinely deep tools before submitting -
thin template apps risk rejection and account strikes.
READMEEOF

APP_COUNT="$(find "$ANDROID_ROOT" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')"
FILE_COUNT="$(find "$OUT" -type f | wc -l | tr -d ' ')"
echo "=============================================="
echo " Done: $APP_COUNT app projects, $FILE_COUNT files"
echo " Location: $OUT"
echo "=============================================="
