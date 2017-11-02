for filename in prolog_web_services/*; do            
    echo $filename
    swipl -f $filename -q main
    echo ""
done

