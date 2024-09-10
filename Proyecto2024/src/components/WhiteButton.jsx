export default function WhiteButton({text}) {
    return (
        <button className="bg-white text-green-900 font-extralight py-2 px-8 rounded-full shadow-md focus:outline-none">
          {text}
        </button>
    );
}