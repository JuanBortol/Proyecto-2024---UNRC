import DarkModeButton from '../components/DarkModeButton'
import WhiteButton from '../components/WhiteButton';

export default function NotLoggedIn() {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center flex-col space-y-8">
          <h1 className="text-6xl font-bold text-white">PROTEINA</h1>
          <hr className="border-t-1 border-white w-12 mx-auto" />
          <WhiteButton text="log in"></WhiteButton>
          <div>
          <DarkModeButton></DarkModeButton>
          </div>
        </div>
      </div>
    );
  }