export default function DarkModeButton({height, className = ''}) {
    return (
        <button className={`rounded-full bg-white border-white flex justify-center items-center ${className}`}>
            <svg enable-background="new 0 0 512 512" height={height} id="Layer_1" version="1.1" viewBox="0 0 512 512" width="32px" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><path d="M248.082,263.932c-31.52-31.542-39.979-77.104-26.02-116.542c-15.25,5.395-29.668,13.833-41.854,26.02  c-43.751,43.75-43.751,114.667,0,158.395c43.729,43.73,114.625,43.752,158.374,0c12.229-12.186,20.646-26.604,26.021-41.854  C325.188,303.91,279.604,295.451,248.082,263.932z" fill="#333333"/></svg>
        </button>
    );
}