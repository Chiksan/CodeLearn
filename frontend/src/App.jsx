import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './store/authStore'
import Navbar from './components/Navbar'
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import CoursesPage from './pages/CoursesPage'
import CoursePage from './pages/CoursePage'
import LessonPage from './pages/LessonPage'
import ProfilePage from './pages/ProfilePage'
import TrackPage from './pages/TrackPage'
import VerifyPage from './pages/VerifyPage'
import LeaderboardPage from './pages/LeaderboardPage'

function PrivateRoute({ children }) {
  const token = useAuthStore(s => s.token)
  return token ? children : <Navigate to="/login" />
}

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/"          element={<HomePage />} />
        <Route path="/login"     element={<LoginPage />} />
        <Route path="/register"  element={<RegisterPage />} />
        <Route path="/courses"         element={<CoursesPage />} />
        <Route path="/courses/:id"     element={<CoursePage />} />
        <Route path="/track/:lang"     element={<TrackPage />} />
        <Route path="/verify"          element={<VerifyPage />} />
        <Route path="/leaderboard"     element={<LeaderboardPage />} />
        <Route path="/lesson/:id" element={
          <PrivateRoute><LessonPage /></PrivateRoute>
        } />
        <Route path="/profile"   element={
          <PrivateRoute><ProfilePage /></PrivateRoute>
        } />
      </Routes>
    </BrowserRouter>
  )
}
