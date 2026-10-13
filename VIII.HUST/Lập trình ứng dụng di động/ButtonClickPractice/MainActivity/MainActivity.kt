/*
 * Bài thực hành: Practice Problem - Button click (Lemonade app)
 * Sinh viên: Bạch Minh Quang - 202490077
 *
 * Ứng dụng mô phỏng 4 bước làm nước chanh:
 *   Bước 1: Chạm vào cây chanh để hái một quả chanh.
 *   Bước 2: Chạm liên tục vào quả chanh để vắt (số lần chạm ngẫu nhiên 2..4).
 *   Bước 3: Chạm vào ly nước chanh để uống.
 *   Bước 4: Chạm vào ly rỗng để bắt đầu lại từ đầu.
 */
package com.example.lemonade

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.Image
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.res.colorResource
import androidx.compose.ui.res.dimensionResource
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.lemonade.ui.theme.LemonadeTheme
import kotlin.random.Random

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            LemonadeTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    LemonadeApp()
                }
            }
        }
    }
}

/**
 * Composable chính của ứng dụng.
 *
 * Trạng thái được lưu trong [currentStep] để giao diện tự cập nhật khi giá trị thay đổi.
 * [squeezeCount] đếm số lần người dùng đã chạm vào quả chanh và được so sánh với
 * [squeezeTarget] - số lần chạm ngẫu nhiên cần thiết để vắt xong quả chanh.
 */
@Composable
fun LemonadeApp() {
    // Bước hiện tại của ứng dụng (1..4). remember giữ giá trị qua các lần recomposition.
    var currentStep by remember { mutableIntStateOf(1) }

    // Số lần cần chạm để vắt xong quả chanh, lấy ngẫu nhiên trong khoảng 2..4.
    var squeezeTarget by remember { mutableIntStateOf(Random.nextInt(2, 5)) }

    // Số lần người dùng đã chạm vào quả chanh ở bước 2.
    var squeezeCount by remember { mutableIntStateOf(0) }

    when (currentStep) {
        // Bước 1: hái chanh từ cây.
        1 -> LemonTextAndImage(
            textLabelResourceId = R.string.lemon_select,
            drawableResourceId = R.drawable.lemon_tree,
            contentDescriptionResourceId = R.string.lemon_tree_content_description,
            onImageClick = {
                currentStep = 2
                squeezeCount = 0
                squeezeTarget = Random.nextInt(2, 5)
            }
        )

        // Bước 2: vắt chanh, yêu cầu chạm nhiều lần.
        2 -> LemonTextAndImage(
            textLabelResourceId = R.string.lemon_squeeze,
            drawableResourceId = R.drawable.lemon_squeeze,
            contentDescriptionResourceId = R.string.lemon_content_description,
            onImageClick = {
                squeezeCount++
                if (squeezeCount >= squeezeTarget) {
                    currentStep = 3
                }
            }
        )

        // Bước 3: uống nước chanh.
        3 -> LemonTextAndImage(
            textLabelResourceId = R.string.lemon_drink,
            drawableResourceId = R.drawable.lemon_drink,
            contentDescriptionResourceId = R.string.lemonade_content_description,
            onImageClick = {
                currentStep = 4
            }
        )

        // Bước 4: ly rỗng, chạm để quay lại bước 1.
        4 -> LemonTextAndImage(
            textLabelResourceId = R.string.lemon_empty_glass,
            drawableResourceId = R.drawable.lemon_restart,
            contentDescriptionResourceId = R.string.empty_glass_content_description,
            onImageClick = {
                currentStep = 1
                squeezeCount = 0
                squeezeTarget = Random.nextInt(2, 5)
            }
        )
    }
}

/**
 * Composable hiển thị một bước làm nước chanh gồm dòng chữ hướng dẫn và hình ảnh có thể chạm.
 *
 * @param textLabelResourceId chuỗi hướng dẫn hiển thị phía trên hình ảnh.
 * @param drawableResourceId hình ảnh minh hoạ của bước hiện tại.
 * @param contentDescriptionResourceId mô tả nội dung hình ảnh dành cho trình đọc màn hình.
 * @param onImageClick hành động được gọi khi người dùng chạm vào hình ảnh.
 */
@Composable
fun LemonTextAndImage(
    textLabelResourceId: Int,
    drawableResourceId: Int,
    contentDescriptionResourceId: Int,
    onImageClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
        modifier = modifier.fillMaxSize()
    ) {
        // Hình ảnh có viền bo góc và xử lý sự kiện chạm.
        Image(
            painter = painterResource(drawableResourceId),
            contentDescription = stringResource(contentDescriptionResourceId),
            modifier = Modifier
                .size(dimensionResource(R.dimen.lemon_image_size))
                .clip(RoundedCornerShape(dimensionResource(R.dimen.border_corner_radius)))
                .border(
                    width = dimensionResource(R.dimen.border_width),
                    color = colorResource(R.color.lemon_border),
                    shape = RoundedCornerShape(dimensionResource(R.dimen.border_corner_radius))
                )
                .clickable { onImageClick() }
        )

        // Khoảng cách giữa hình ảnh và dòng chữ.
        Spacer(modifier = Modifier.height(dimensionResource(R.dimen.text_image_padding)))

        Text(
            text = stringResource(textLabelResourceId),
            fontSize = dimensionResource(R.dimen.text_size).value.sp
        )
    }
}

@Preview(showBackground = true)
@Composable
fun LemonadeAppPreview() {
    LemonadeTheme {
        LemonadeApp()
    }
}
