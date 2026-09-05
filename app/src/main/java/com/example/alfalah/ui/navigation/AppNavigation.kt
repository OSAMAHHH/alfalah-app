package com.example.alfalah.ui.navigation

import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.DateRange
import androidx.compose.material.icons.filled.MenuBook
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.Chat
import androidx.compose.material3.Icon
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.navigation.NavDestination.Companion.hierarchy
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import com.example.alfalah.data.repository.AuthRepository
import com.example.alfalah.ui.screens.auth.LoginScreen
import com.example.alfalah.ui.screens.auth.RegisterScreen
import com.example.alfalah.ui.screens.chat.ConversationsScreen
import com.example.alfalah.ui.screens.chat.ChatScreen
import com.example.alfalah.ui.screens.guide.GuideScreen
import com.example.alfalah.ui.screens.guide.CropDetailsScreen
import com.example.alfalah.ui.screens.guide.ProblemDetailsScreen
import com.example.alfalah.ui.screens.home.HomeScreen
import com.example.alfalah.ui.screens.calendar.CalendarScreen
import com.example.alfalah.ui.screens.profile.ProfileScreen
import com.example.alfalah.ui.screens.profile.FavoritesScreen
import com.example.alfalah.ui.screens.profile.MyOrdersScreen
import com.example.alfalah.ui.screens.store.CheckoutScreen
import com.example.alfalah.ui.screens.store.CartScreen
import com.example.alfalah.ui.screens.store.ProductDetailsScreen
import com.example.alfalah.ui.screens.admin.AdminDashboardScreen
import com.example.alfalah.ui.screens.admin.AdminOrdersScreen
import com.example.alfalah.ui.screens.admin.ImportDatabaseScreen

@Composable
fun AppNavigation() {
    val navController = rememberNavController()
    val authRepository = remember { AuthRepository() }
    val startDestination = "main"

    NavHost(navController = navController, startDestination = startDestination) {
        composable("login") {
            LoginScreen(
                authRepository = authRepository,
                onNavigateToRegister = { navController.navigate("register") },
                onLoginSuccess = {
                    navController.navigate("main") {
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
                    navController.navigate("main") {
                        popUpTo(0)
                    }
                }
            )
        }
        composable("main") {
            MainScreen(authRepository = authRepository, onLogout = {
                authRepository.logout()
                navController.navigate("login") { popUpTo(0) }
            })
        }
    }
}

@Composable
fun MainScreen(authRepository: AuthRepository, onLogout: () -> Unit) {
    val navController = rememberNavController()
    
    val items = listOf(
        Pair("home", "الرئيسية") to Icons.Filled.Home,
        Pair("guide", "الدليل") to Icons.Filled.MenuBook,
        Pair("calendar", "التقويم") to Icons.Filled.DateRange,
        Pair("conversations", "المساعد") to Icons.Filled.Chat,
        Pair("profile", "حسابي") to Icons.Filled.Person
    )

    Scaffold(
        bottomBar = {
            val navBackStackEntry by navController.currentBackStackEntryAsState()
            val currentDestination = navBackStackEntry?.destination
            
            // Hide bottom bar in sub-screens
            val showBottomBar = items.any { it.first.first == currentDestination?.route }
            
            if (showBottomBar) {
                NavigationBar {
                    items.forEach { (routePair, icon) ->
                        val (route, label) = routePair
                        NavigationBarItem(
                            icon = { Icon(icon, contentDescription = label) },
                            label = { Text(label) },
                            selected = currentDestination?.hierarchy?.any { it.route == route } == true,
                            onClick = {
                                navController.navigate(route) {
                                    popUpTo(navController.graph.findStartDestination().id) {
                                        saveState = true
                                    }
                                    launchSingleTop = true
                                    restoreState = true
                                }
                            }
                        )
                    }
                }
            }
        }
    ) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = "home",
            modifier = Modifier.padding(innerPadding)
        ) {
            composable("home") {
                HomeScreen(
                    authRepository = authRepository,
                    onNavigateToGuide = { cat -> navController.navigate("guide") },
                    onNavigateToCrop = { id -> navController.navigate("crop/$id") },
                    onNavigateToProduct = { id -> navController.navigate("product/$id") },
                    onNavigateToStore = { navController.navigate("store") },
                    onNavigateToAdmin = { navController.navigate("adminDashboard") },
                    onNavigateToChat = { navController.navigate("conversations") },
                    onNavigateToCart = { navController.navigate("cart") },
                    onLogout = onLogout
                )
            }
            composable("store") {
                com.example.alfalah.ui.screens.store.StoreScreen(
                    onBack = { navController.popBackStack() },
                    onNavigateToProduct = { id -> navController.navigate("product/$id") },
                    onNavigateToCart = { navController.navigate("cart") }
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
            composable("calendar") {
                CalendarScreen(
                    onNavigateToCrop = { id -> navController.navigate("crop/$id") }
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
                    onNavigateToCart = { navController.navigate("cart") }
                )
            }
            composable("profile") {
                ProfileScreen(
                    authRepository = authRepository,
                    onBack = { navController.popBackStack() },
                    onNavigateToFavorites = { navController.navigate("favorites") },
                    onNavigateToMyOrders = { navController.navigate("myOrders") },
                    onNavigateToAdmin = { navController.navigate("adminDashboard") },
                    onNavigateToSettings = { navController.navigate("settings") },
                    onNavigateToMyCrops = { navController.navigate("myCrops") },
                    onNavigateToConversations = { navController.navigate("conversations") },
                    onLogout = onLogout
                )
            }
            composable("settings") {
                com.example.alfalah.ui.screens.profile.SettingsScreen(onLogout = onLogout, 
                    onBack = { navController.popBackStack() }
                )
            }
            composable("myCrops") {
                com.example.alfalah.ui.screens.profile.MyCropsScreen(
                    onBack = { navController.popBackStack() },
                    onNavigateToCrop = { id -> navController.navigate("crop/$id") }
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
            composable("cart") {
                CartScreen(
                    onBack = { navController.popBackStack() },
                    onCheckout = { navController.navigate("checkout") }
                )
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
}
