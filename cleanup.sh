#!/bin/bash
if [ $# -lt 1 ]; then
  echo "usage:"
  echo "    cleanup.sh <language>"
  echo ""
  echo "for example"
  echo "    ./cleanup.sh en"
  echo "    ./cleanup.sh de"
  echo ""
  echo "This program removes all temorary files which are created by"
  echo "pdflatex schlizbaedas_Phoniebox_<language>"
  exit 1
fi
echo "cleaning up for language version '$1':"
if [ -d chapter/$1 ]; then
  # The language implementation exists in chapters: Clean up
  rm schlizbaedas_Phoniebox_$1.aux schlizbaedas_Phoniebox_$1.idx schlizbaedas_Phoniebox_$1.lo? schlizbaedas_Phoniebox_$1.nlo schlizbaedas_Phoniebox_$1.out schlizbaedas_Phoniebox_$1.toc
  rm chapter/$1/*.aux
  rm layout/*.aux layout/$1/*.aux
else  
  echo "The project schlizbaedas_Phoniebox doesn't exist"
  echo "for language '$1' yet." 
  echo "But don't hesitate to add it :-)" 
  exit 2
fi

