package com.example.alfalah.ui.navigation

import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.alfalah.data.repository.AuthRepository
import com.example.alfalah.ui.screens.auth.LoginScreen
import com.example.alfalah.ui.screens.auth.RegisterScreen
import com.example.alfalah.ui.screens.chat.ConversationsScreen
import com.example.alfalah.ui.screens.chat.ChatScreen
import com.example.alfalah.ui.screens.guide.GuideScreen
import com.example.alfalah.ui.screens.guide.CropDetailsScreen
import com.example.alfalah.ui.screens.guide.ProblemDetailsScreen
import com.example.alfalah.ui.screens.profile.ProfileScreen
import com.example.alfalah.ui.screens.profile.FavoritesScreen
import com.example.alfalah.ui.screens.profile.MyOrdersScreen
import com.example.alfalah.ui.screens.store.CheckoutScreen
import com.example.alfalah.ui.screens.store.ProductDetailsScreen
import com.example.alfalah.ui.screens.admin.AdminDashboardScreen
import com.example.alfalah.ui.screens.admin.AdminOrdersScreen
import com.example.alfalah.ui.screens.admin.ImportDatabaseScreen

@Composable
fun AppNavigation() {
    val navController = rememberNavController()
    val authRepository = remember { AuthRepository() }

    val startDestination = if (authRepository.currentUser.value != null) "guide" else "login"

    NavHost(navController = navController, startDestination = startDestination) {
        composable("login") {
            LoginScreen(
                authRepository = authRepository,
                onNavigateToRegister = { navController.navigate("register") },
                onLoginSuccess = {
                    navController.navigate("guide") {
                        popUpTo(0)
                    }
                }
            )
        }
        composable("register") {
            RegisterScreen(
                authRepository = authRepository,
                onNavigateToLogin = { navController.popBackStack() },
                onRegisterSuccess = {
                    navController.navigate("guide") {
                        popUpTo(0)
                    }
                }
            )
        }
        composable("guide") {
            GuideScreen(
                category = "crops",
                onBack = { navController.popBackStack() },
                onNavigateToCrop = { id -> navController.navigate("crop/$id") },
                onNavigateToProblem = { id -> navController.navigate("problem/$id") }
            )
        }
        composable("crop/{id}") { backStackEntry ->
            val id = backStackEntry.arguments?.getString("id") ?: return@composable
            CropDetailsScreen(
                cropId = id,
                onBack = { navController.popBackStack() },
                onNavigateToProblem = { pId -> navController.navigate("problem/$pId") },
                onNavigateToChatWithQuery = { query -> navController.navigate("chat?initialQuery=$query") }
            )
        }
        composable("problem/{id}") { backStackEntry ->
            val id = backStackEntry.arguments?.getString("id") ?: return@composable
            ProblemDetailsScreen(
                problemId = id,
                onBack = { navController.popBackStack() },
                onNavigateToProduct = { pId -> navController.navigate("product/$pId") },
                onNavigateToChatWithQuery = { query -> navController.navigate("chat?initialQuery=$query") }
            )
        }
        composable("product/{id}") { backStackEntry ->
            val id = backStackEntry.arguments?.getString("id") ?: return@composable
            ProductDetailsScreen(
                productId = id,
                onBack = { navController.popBackStack() },
                onNavigateToCart = { navController.navigate("checkout") }
            )
        }
        composable("profile") {
            ProfileScreen(
                authRepository = authRepository,
                onBack = { navController.popBackStack() },
                onNavigateToFavorites = { navController.navigate("favorites") },
                onNavigateToMyOrders = { navController.navigate("myOrders") },
                onNavigateToAdmin = { navController.navigate("adminDashboard") },
                onLogout = {
                    authRepository.logout()
                    navController.navigate("login") {
                        popUpTo(0)
                    }
                }
            )
        }
        composable("favorites") {
            FavoritesScreen(
                onBack = { navController.popBackStack() },
                onNavigateToProduct = { pId -> navController.navigate("product/$pId") },
                onNavigateToCrop = { cId -> navController.navigate("crop/$cId") },
                onNavigateToProblem = { pId -> navController.navigate("problem/$pId") }
            )
        }
        composable("myOrders") {
            MyOrdersScreen(
                onBack = { navController.popBackStack() }
            )
        }
        composable("conversations") {
            ConversationsScreen(
                onBack = { navController.popBackStack() },
                onNavigateToChat = { convId -> navController.navigate("chat?id=$convId") }
            )
        }
        composable(
            route = "chat?id={id}&initialQuery={initialQuery}",
            arguments = listOf(
                androidx.navigation.navArgument("id") { nullable = true },
                androidx.navigation.navArgument("initialQuery") { nullable = true }
            )
        ) { backStackEntry ->
            val id = backStackEntry.arguments?.getString("id")
            val query = backStackEntry.arguments?.getString("initialQuery")
            ChatScreen(
                conversationId = id,
                onBack = { navController.popBackStack() },
                onNavigateToProduct = { pId -> navController.navigate("product/$pId") },
                initialQuery = query
            )
        }
        composable("adminDashboard") {
            AdminDashboardScreen(
                onBack = { navController.popBackStack() },
                onNavigateToImport = { navController.navigate("importDb") }
            )
        }
        composable("adminOrders") {
            AdminOrdersScreen()
        }
        composable("checkout") {
            CheckoutScreen(
                onBack = { navController.popBackStack() },
                onOrderSuccess = { navController.navigate("myOrders") }
            )
        }
        composable("importDb") {
            ImportDatabaseScreen(
                onBack = { navController.popBackStack() }
            )
        }
    }
}
