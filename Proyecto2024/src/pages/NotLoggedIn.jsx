import DarkModeButton from '../components/DarkModeButton'
import styles from '../styles/NotLoggedIn.module.css'

export default function NotLoggedIn() {
    return (
      <div className={`flex items-center justify-center min-h-screen ${styles.bgGradient}`}>
        <div className="text-center flex-col space-y-8 flex items-center">
          <h1 className="text-6xl font-bold text-white">PROTEINA</h1>
          <hr className="border-t-1 border-white w-12 mx-auto" />
          <button className="bg-white text-green-950 font-extralight py-2 px-8 rounded-full shadow-md focus:outline-none">
            log in
          </button>
          <div>
          <DarkModeButton height='32px'/>
          </div>
        </div>
      </div>
    );
  }