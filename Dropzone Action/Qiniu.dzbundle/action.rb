# Dropzone Action Info
# Name: Qiniu
# Description: Upload file to Qiniu
# Handles: Files
# Creator: Su Yan
# URL: http://yansu.org
# OptionsNIB: ExtendedLogin
# Events: Clicked, Dragged
# KeyModifiers: Command, Option, Control, Shift
# SkipConfig: No
# RunsSandboxed: Yes
# Version: 1.0
# MinDropzoneVersion: 3.0
# RubyPath: /usr/bin/ruby
 
require 'qiniu'
 
Qiniu.establish_connection! :access_key => ENV['username'],
                            :secret_key => ENV['password']
 
ENV['http_proxy'] = ""
 
def dragged
  puts $items.inspect
  local_file = $items[0]
  puts local_file
  
  put_policy = Qiniu::Auth::PutPolicy.new(ENV['server'], File.basename(local_file))
  uptoken = Qiniu::Auth.generate_uptoken(put_policy)
  puts uptoken
  
  $dz.begin("Starting uploading...")
  $dz.determinate(true)
  $dz.percent(10)

  # copy to folder
  Rsync.do_copy([local_file], ENV['remote_path'], false)

  $dz.percent(30)
   
  code, result, response_headers = Qiniu::Storage.upload_with_put_policy(
    put_policy,
    local_file
  )
 
  $dz.percent(60)
  
  puts code
  puts result
  puts response_headers
 
  $dz.percent(100)
  $dz.finish("Url has been copied to clipboard.")
  
  if code != 200
    $dz.fail("Error uploading file")
  else
    url = "#{ENV["root_url"]}/#{result["key"]}"
    $dz.url(url)
  end
end
 
def clicked
  system("open http://qiniu.com")
end