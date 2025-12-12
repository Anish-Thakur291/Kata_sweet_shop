param(
  [Parameter(ValueFromRemainingArguments=$true)]
  $args
)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$manage = Join-Path $scriptDir "..\manage.py"
python $manage @args
