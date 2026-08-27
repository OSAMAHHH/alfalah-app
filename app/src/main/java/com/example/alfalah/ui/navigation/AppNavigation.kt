package com.example.alfalah.ui.navigation

import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.alfalah.data.repository.AuthRepository
import com.example.alfalah.ui.screens.auth.LoginScreen
import com.example.alfalah.ui.screens.auth.RegisterScreen
import com.example.alfalah.ui.screens.home.HomeScreen
import com.example.alfalah.ui.screens.store.StoreScreen
import com.example.alfalah.ui.screens.store.ProductDetailsScreen
import com.example.alfalah.ui.screens.chat.ChatScreen
import com.example.alfalah.ui.screens.admin.AdminDashboardScreen

object Routes {
    const val LOGIN = "login"
    const val REGISTER = "register"
    const val HOME = "home"
    const val STORE = "store"
    const val CHAT = "chat"
    const val ADMIN_DASHBOARD = "admin_dashboard"
    const val PRODUCT_DETAILS = "product_details/{productId}"
    fun productDetails(id: String) = "product_details/$id"
}

@Composable
fun AppNavigation(authRepository: AuthRepository = AuthRepository()) {
    val navController = rememberNavController()
    val currentUser by authRepository.currentUser.collectAsState()

    NavHost(
        navController = navController,
        startDestination = if (currentUser != null) Routes.HOME else Routes.LOGIN
    ) {
        composable(Routes.LOGIN) {
            LoginScreen(
                authRepository = authRepository,
                onNavigateToRegister = { navController.navigate(Routes.REGISTER) },
                onLoginSuccess = { navController.navigate(Routes.HOME) { popUpTo(Routes.LOGIN) { inclusive = true } } }
            )
        }
        composable(Routes.REGISTER) {
            RegisterScreen(
                authRepository = authRepository,
                onNavigateToLogin = { navController.navigate(Routes.LOGIN) },
                onRegisterSuccess = { navController.navigate(Routes.HOME) { popUpTo(Routes.REGISTER) { inclusive = true } } }
            )
        }
        composable(Routes.HOME) {
            HomeScreen(
                authRepository = authRepository,
                onNavigateToStore = { navController.navigate(Routes.STORE) },
                onNavigateToChat = { navController.navigate(Routes.CHAT) },
                onNavigateToAdmin = { navController.navigate(Routes.ADMIN_DASHBOARD) },
                onLogout = { navController.navigate(Routes.LOGIN) { popUpTo(Routes.HOME) { inclusive = true } } }
            )
        }
        composable(Routes.STORE) {
            StoreScreen(
                onBack = { navController.popBackStack() },
                onNavigateToProduct = { id -> navController.navigate(Routes.productDetails(id)) }
            )
        }
        composable(Routes.CHAT) {
            ChatScreen(
                onBack = { navController.popBackStack() },
                onNavigateToProduct = { id -> navController.navigate(Routes.productDetails(id)) }
            )
        }
        composable(Routes.ADMIN_DASHBOARD) {
            AdminDashboardScreen(
                onBack = { navController.popBackStack() }
            )
        }
        composable(Routes.PRODUCT_DETAILS) { backStackEntry ->
            val productId = backStackEntry.arguments?.getString("productId") ?: ""
            ProductDetailsScreen(
                productId = productId,
                onBack = { navController.popBackStack() }
            )
        }
    }
}
