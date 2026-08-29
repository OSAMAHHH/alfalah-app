package com.example.alfalah.ui.navigation

import androidx.compose.animation.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.SmartToy
import androidx.compose.material.icons.filled.Store
import androidx.compose.material.icons.outlined.Home
import androidx.compose.material.icons.outlined.SmartToy
import androidx.compose.material.icons.outlined.Store
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.navigation.NavDestination.Companion.hierarchy
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.compose.*
import com.example.alfalah.data.repository.AuthRepository
import com.example.alfalah.ui.screens.admin.AdminDashboardScreen
import com.example.alfalah.ui.screens.auth.LoginScreen
import com.example.alfalah.ui.screens.auth.RegisterScreen
import com.example.alfalah.ui.screens.chat.ChatScreen
import com.example.alfalah.ui.screens.home.HomeScreen
import com.example.alfalah.ui.screens.guide.GuideScreen
import com.example.alfalah.ui.screens.store.ProductDetailsScreen
import com.example.alfalah.ui.screens.store.StoreScreen
import com.google.firebase.auth.FirebaseAuth

object Routes {
    const val LOGIN = "login"
    const val REGISTER = "register"
    const val HOME = "home"
    const val STORE = "store"
    const val CHAT = "chat"
    const val GUIDE = "guide/{category}"
    fun guide(category: String) = "guide/$category"
    const val ADMIN_DASHBOARD = "admin_dashboard"
    const val PRODUCT_DETAILS = "product_details/{productId}"
    fun productDetails(id: String) = "product_details/$id"
}

data class BottomNavItem(
    val route: String,
    val title: String,
    val selectedIcon: androidx.compose.ui.graphics.vector.ImageVector,
    val unselectedIcon: androidx.compose.ui.graphics.vector.ImageVector
)

val bottomNavItems = listOf(
    BottomNavItem(Routes.HOME, "الرئيسية", Icons.Filled.Home, Icons.Outlined.Home),
    BottomNavItem(Routes.STORE, "المتجر", Icons.Filled.Store, Icons.Outlined.Store),
    BottomNavItem(Routes.CHAT, "المساعد", Icons.Filled.SmartToy, Icons.Outlined.SmartToy)
)

@Composable
fun AppNavigation(authRepository: AuthRepository = AuthRepository()) {
    val navController = rememberNavController()
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentDestination = navBackStackEntry?.destination
    val currentRoute = currentDestination?.route

    val showBottomBar = currentRoute in listOf(Routes.HOME, Routes.STORE, Routes.CHAT)

    // Evaluate startDestination exactly once when the NavHost is created.
    // This prevents the NavHost from rebuilding/flickering when AuthRepository finishes fetching from Firestore.
    val startDestination = remember {
        if (FirebaseAuth.getInstance().currentUser != null) Routes.HOME else Routes.LOGIN
    }

    Scaffold(
        bottomBar = {
            AnimatedVisibility(
                visible = showBottomBar,
                enter = slideInVertically(initialOffsetY = { it }),
                exit = slideOutVertically(targetOffsetY = { it })
            ) {
                Surface(
                    modifier = Modifier
                        .padding(start = 24.dp, end = 24.dp, bottom = 24.dp)
                        .fillMaxWidth(),
                    shape = RoundedCornerShape(32.dp),
                    shadowElevation = 16.dp,
                    color = MaterialTheme.colorScheme.surface
                ) {
                    NavigationBar(
                        containerColor = androidx.compose.ui.graphics.Color.Transparent,
                        tonalElevation = 0.dp,
                        modifier = Modifier.height(72.dp)
                    ) {
                        bottomNavItems.forEach { item ->
                            val isSelected = currentDestination?.hierarchy?.any { it.route == item.route } == true
                            NavigationBarItem(
                                icon = { Icon(if (isSelected) item.selectedIcon else item.unselectedIcon, contentDescription = item.title) },
                                label = { Text(item.title, fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal) },
                                selected = isSelected,
                                colors = NavigationBarItemDefaults.colors(
                                    selectedIconColor = MaterialTheme.colorScheme.onPrimaryContainer,
                                    unselectedIconColor = MaterialTheme.colorScheme.onSurfaceVariant,
                                    selectedTextColor = MaterialTheme.colorScheme.primary,
                                    unselectedTextColor = MaterialTheme.colorScheme.onSurfaceVariant,
                                    indicatorColor = MaterialTheme.colorScheme.primaryContainer
                                ),
                                onClick = {
                                    navController.navigate(item.route) {
                                        popUpTo(navController.graph.findStartDestination().id) { saveState = true }
                                        launchSingleTop = true
                                        restoreState = true
                                    }
                                }
                            )
                        }
                    }
                }
            }
        }
    ) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = startDestination,
            modifier = Modifier.padding(bottom = if (showBottomBar) 96.dp else 0.dp)
        ) {
            composable(Routes.LOGIN) {
                LoginScreen(
                    authRepository = authRepository,
                    onNavigateToRegister = { navController.navigate(Routes.REGISTER) },
                    onLoginSuccess = { 
                        navController.navigate(Routes.HOME) { 
                            popUpTo(Routes.LOGIN) { inclusive = true } 
                        } 
                    }
                )
            }
            composable(Routes.REGISTER) {
                RegisterScreen(
                    authRepository = authRepository,
                    onNavigateToLogin = { navController.navigate(Routes.LOGIN) },
                    onRegisterSuccess = { 
                        navController.navigate(Routes.HOME) { 
                            popUpTo(Routes.LOGIN) { inclusive = true } 
                        } 
                    }
                )
            }
            composable(Routes.HOME) {
                HomeScreen(
                    authRepository = authRepository,
                    onNavigateToStore = { 
                        navController.navigate(Routes.STORE) { 
                            popUpTo(navController.graph.findStartDestination().id) { saveState = true }
                            launchSingleTop = true
                            restoreState = true 
                        } 
                    },
                    onNavigateToChat = { 
                        navController.navigate(Routes.CHAT) { 
                            popUpTo(navController.graph.findStartDestination().id) { saveState = true }
                            launchSingleTop = true
                            restoreState = true 
                        } 
                    },
                    onNavigateToAdmin = { navController.navigate(Routes.ADMIN_DASHBOARD) },
                    onNavigateToGuide = { category -> navController.navigate(Routes.guide(category)) },
                    onLogout = { 
                        navController.navigate(Routes.LOGIN) { 
                            popUpTo(Routes.HOME) { inclusive = true } 
                        } 
                    }
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
            composable(Routes.GUIDE) { backStackEntry ->
                val category = backStackEntry.arguments?.getString("category") ?: ""
                GuideScreen(category = category, onBack = { navController.popBackStack() })
            }
            composable(Routes.ADMIN_DASHBOARD) { 
                AdminDashboardScreen(onBack = { navController.popBackStack() }) 
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
}
