$size = "M"

if ($size -e "S"){
	Write-Host "Small"
} elseif($size -eq "M") {
	Write-Host "Medium"
} else {
	Write-Host "Large"
} 

