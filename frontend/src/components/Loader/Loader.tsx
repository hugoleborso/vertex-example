import { faSpinner } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

export const Loader = () => {
    return (
      <div className="h-full w-full flex items-center justify-center">
        <FontAwesomeIcon
          icon={faSpinner}
          pulse
          spin
          className="animate-spin m-auto"
        />
      </div>
    );
  };
  