#!/usr/bin/env bash

INSDIR="/opt/instinctual"
INSTALLDIR="$INSDIR/teradicislider"

cd "$(dirname "$0")" || exit
CURRENTDIR=`pwd`
cd $CURRENTDIR

# If the script is not running as root, it won't have permissions to install packages.
# So, check if the user has root privileges
if [[ $UID -ne 0 ]]; then
    echo "You must be root to install packages. Try running with sudo or as root."
    exit 1
fi

show_usage() {
    echo "Usage: $0 [--install | --uninstall]"
    echo "  --install       Install Teradici Slider"
    echo "  --uninstall     Un-install Teradici Slider"
}

check_internet(){
 echo "Testing for Internet connectivity to google.com.  Please wait."
      ping -W2 -c1 google.com > /dev/null
      if [ $? -eq 0 ]
        then
          echo "Internet is good.  Moving On."
          echo
        else
          echo "Installer needs Internet connectivity. Open the firewall and try again."
          exit 0
      fi
      }

# No options means we should display usage
if [[ $# -eq 0 ]]; then
    show_usage
    exit 1
fi

# Save the option in a variable
ACTION=""

while [[ "$1" != "" ]]; do
    case $1 in
        --install)
            shift
            ACTION="install"
            ;;
        --uninstall)
            shift
            ACTION="uninstall"
            ;;
        *)
            echo "Invalid option: $1" >&2
            show_usage
            exit 1
            ;;
    esac
done

if [[ $ACTION == "install" ]]; then
  # Check if xmlstarlet is installed
  if ! rpm -q crudini &>/dev/null; then
      echo
      echo "crudini is NOT installed."
      read -p "Do you want to install crudini? This will also install epel-release and requires an Internet Connection. (y/n) " choice

      case $choice in
          y|Y)
              check_internet
              # Attempt to install crudini
              dnf install -y epel-release
              dnf update -y epel-release
              dnf install -y crudini
              ;;
          n|N)
              echo "Exiting without installing crudini."
              exit 1
              ;;
          *)
              echo "Invalid choice. Exiting."
              exit 1
              ;;
      esac
  fi

    mkdir -p "$INSTALLDIR"
    install -m 555 teradicislider.py "$INSTALLDIR"
    install -m 444 teradicislider.png "$INSTALLDIR"
    install -m 440 teradicislider.rules /etc/sudoers.d/teradicislider
    install -m 444 teradicislider.desktop /usr/share/applications/teradicislider.desktop

    /usr/bin/crudini --set /etc/pcoip-agent/pcoip-agent.conf "quality" pcoip.maximum_initial_image_quality 80

    echo "Teradici Slider has been installed."

elif [[ "$ACTION" == "uninstall" ]]; then

  rm -vf /etc/sudoers.d/teradicislider
  rm -vf /usr/share/applications/teradicislider.desktop
  rm -vrf "$INSTALLDIR"
  
  # Check if the INSDIR
  if [[ -d $INSDIR ]]; then
      # Check if the INSDIR is empty
      if [[ ! "$(ls -A "$INSDIR")" ]]; then
          echo "Directory "$INSDIR" is empty. Deleting..."
          rmdir -v "$INSDIR"
          if [[ $? -eq 0 ]]; then
              echo "Directory "$INSDIR" successfully deleted."
          else
              echo "Failed to delete $INSDIR."
          fi
      else
          echo "Directory $INSDIR is not empty. Not deleting."
      fi
  else
      echo "Directory $INSDIR does not exist."
  fi
  echo "Teradici Slider has been un-installed."
fi
