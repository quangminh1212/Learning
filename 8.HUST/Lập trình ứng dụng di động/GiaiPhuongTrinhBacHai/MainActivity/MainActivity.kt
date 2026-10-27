package com.example.ptbac2

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import java.math.BigDecimal

private val Ink = Color(0xFF14213D)
private val Muted = Color(0xFF64748B)
private val Blue = Color(0xFF2457D6)
private val Canvas = Color(0xFFF3F6FC)
private val Green = Color(0xFF087F5B)
private val Red = Color(0xFFB42318)

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                Surface(modifier = Modifier.fillMaxSize(), color = Canvas) {
                    QuadraticEquationScreen()
                }
            }
        }
    }
}

private data class SolveResult(
    val title: String,
    val message: String,
    val delta: String? = null,
    val roots: List<String> = emptyList(),
    val isError: Boolean = false
)

@Composable
private fun QuadraticEquationScreen() {
    var a by remember { mutableStateOf("1") }
    var b by remember { mutableStateOf("-3") }
    var c by remember { mutableStateOf("2") }
    var result by remember { mutableStateOf<SolveResult?>(null) }
    val focusManager = LocalFocusManager.current

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Canvas)
            .verticalScroll(rememberScrollState())
            .padding(horizontal = 22.dp, vertical = 28.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            text = "TOÁN HỌC  •  TIỆN ÍCH",
            color = Blue,
            fontSize = 12.sp,
            fontWeight = FontWeight.Bold,
            letterSpacing = 1.4.sp
        )
        Spacer(Modifier.height(10.dp))
        Text(
            text = "Giải phương trình\nbậc hai",
            color = Ink,
            fontSize = 30.sp,
            lineHeight = 36.sp,
            fontWeight = FontWeight.Bold,
            textAlign = TextAlign.Center
        )
        Spacer(Modifier.height(10.dp))
        Text(
            text = "Nhập các hệ số a, b, c để tìm nghiệm",
            color = Muted,
            fontSize = 14.sp,
            textAlign = TextAlign.Center
        )
        Spacer(Modifier.height(24.dp))

        Card(
            modifier = Modifier.fillMaxWidth(),
            shape = RoundedCornerShape(22.dp),
            colors = CardDefaults.cardColors(containerColor = Color.White),
            elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
        ) {
            Column(Modifier.padding(20.dp)) {
                Text("PHƯƠNG TRÌNH", color = Muted, fontSize = 11.sp, fontWeight = FontWeight.Bold, letterSpacing = 1.sp)
                Spacer(Modifier.height(8.dp))
                Text("ax² + bx + c = 0", color = Ink, fontSize = 23.sp, fontWeight = FontWeight.SemiBold)
                Spacer(Modifier.height(20.dp))

                CoefficientField(label = "Hệ số a", value = a, onValueChange = { a = it })
                Spacer(Modifier.height(12.dp))
                CoefficientField(label = "Hệ số b", value = b, onValueChange = { b = it })
                Spacer(Modifier.height(12.dp))
                CoefficientField(label = "Hệ số c", value = c, onValueChange = { c = it })
                Spacer(Modifier.height(20.dp))

                Button(
                    onClick = {
                        focusManager.clearFocus()
                        result = solveEquation(a, b, c)
                    },
                    modifier = Modifier.fillMaxWidth().height(54.dp),
                    shape = RoundedCornerShape(15.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = Blue)
                ) {
                    Text("GIẢI PHƯƠNG TRÌNH", fontWeight = FontWeight.Bold, letterSpacing = 0.4.sp)
                }
                TextButton(
                    onClick = {
                        a = ""
                        b = ""
                        c = ""
                        result = null
                    },
                    modifier = Modifier.align(Alignment.CenterHorizontally)
                ) {
                    Text("Xóa dữ liệu", color = Muted)
                }
            }
        }

        result?.let { output ->
            Spacer(Modifier.height(18.dp))
            ResultCard(output)
        }

        Spacer(Modifier.height(18.dp))
        Text(
            text = "Hỗ trợ nghiệm thực và phương trình suy biến",
            color = Muted,
            fontSize = 12.sp,
            textAlign = TextAlign.Center
        )
    }
}

@Composable
private fun CoefficientField(label: String, value: String, onValueChange: (String) -> Unit) {
    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth()) {
        Text(label, modifier = Modifier.width(84.dp), color = Ink, fontWeight = FontWeight.Medium, fontSize = 14.sp)
        OutlinedTextField(
            value = value,
            onValueChange = { input ->
                if (input.length <= 18 && input.matches(Regex("[-+]?[0-9]*[.,]?[0-9]*"))) onValueChange(input)
            },
            modifier = Modifier.weight(1f),
            singleLine = true,
            placeholder = { Text("Nhập hệ số", color = Muted.copy(alpha = 0.6f)) },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
            shape = RoundedCornerShape(13.dp),
            colors = OutlinedTextFieldDefaults.colors(
                focusedBorderColor = Blue,
                unfocusedBorderColor = Color(0xFFD8E0ED),
                focusedContainerColor = Color.White,
                unfocusedContainerColor = Color.White
            )
        )
    }
}

@Composable
private fun ResultCard(result: SolveResult) {
    val accent = if (result.isError) Red else Green
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(20.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(Modifier.fillMaxWidth().padding(20.dp)) {
            Text("KẾT QUẢ", color = Muted, fontSize = 11.sp, fontWeight = FontWeight.Bold, letterSpacing = 1.sp)
            Spacer(Modifier.height(8.dp))
            Text(result.title, color = accent, fontSize = 19.sp, fontWeight = FontWeight.Bold)
            Spacer(Modifier.height(5.dp))
            Text(result.message, color = Ink, fontSize = 14.sp)
            result.delta?.let {
                Spacer(Modifier.height(12.dp))
                Text("Δ = $it", color = Muted, fontSize = 14.sp)
            }
            if (result.roots.isNotEmpty()) {
                Spacer(Modifier.height(12.dp))
                result.roots.forEach { root ->
                    Text(root, color = Ink, fontSize = 17.sp, fontWeight = FontWeight.SemiBold)
                    Spacer(Modifier.height(4.dp))
                }
            }
        }
    }
}

private fun solveEquation(aText: String, bText: String, cText: String): SolveResult {
    fun parse(value: String): Double? = value.trim().replace(',', '.').toDoubleOrNull()?.takeIf { it.isFinite() }

    val a = parse(aText)
    val b = parse(bText)
    val c = parse(cText)
    if (a == null || b == null || c == null) {
        return SolveResult("Chưa thể giải", "Vui lòng nhập đầy đủ ba hệ số hợp lệ.", isError = true)
    }

    if (a == 0.0) {
        if (b == 0.0) {
            return if (c == 0.0) {
                SolveResult("Vô số nghiệm", "Mọi giá trị x đều thỏa mãn phương trình.")
            } else {
                SolveResult("Vô nghiệm", "Phương trình không có giá trị x thỏa mãn.")
            }
        }
        val x = -c / b
        return if (x.isFinite()) {
            SolveResult("Phương trình bậc nhất", "Vì a = 0 nên phương trình trở thành bx + c = 0.", roots = listOf("x = ${formatNumber(x)}"))
        } else {
            SolveResult("Giá trị quá lớn", "Kết quả vượt quá phạm vi tính toán.", isError = true)
        }
    }

    val delta = b * b - 4.0 * a * c
    if (!delta.isFinite()) {
        return SolveResult("Giá trị quá lớn", "Không thể tính biệt thức với các hệ số này.", isError = true)
    }
    val deltaText = formatNumber(delta)
    return when {
        delta > 0.0 -> {
            val sqrtDelta = kotlin.math.sqrt(delta)
            val x1 = (-b + sqrtDelta) / (2.0 * a)
            val x2 = (-b - sqrtDelta) / (2.0 * a)
            if (!x1.isFinite() || !x2.isFinite()) {
                SolveResult("Giá trị quá lớn", "Nghiệm vượt quá phạm vi tính toán.", delta = deltaText, isError = true)
            } else {
                SolveResult(
                    "Có hai nghiệm phân biệt",
                    "Vì Δ > 0, phương trình có hai nghiệm thực.",
                    delta = deltaText,
                    roots = listOf("x₁ = ${formatNumber(x1)}", "x₂ = ${formatNumber(x2)}")
                )
            }
        }
        delta == 0.0 -> {
            val x = -b / (2.0 * a)
            SolveResult("Có nghiệm kép", "Vì Δ = 0, phương trình có một nghiệm kép.", delta = deltaText, roots = listOf("x = ${formatNumber(x)}"))
        }
        else -> SolveResult("Vô nghiệm thực", "Vì Δ < 0, phương trình không có nghiệm trong tập số thực.", delta = deltaText)
    }
}

private fun formatNumber(value: Double): String =
    BigDecimal.valueOf(if (value == 0.0) 0.0 else value).stripTrailingZeros().toPlainString().replace('.', ',')
