Gem::Specification.new do |s|
  s.name        = 'empressiza-plant-matrix'
  s.version     = '1.0.0'
  s.summary     = "Programmatic open-source botanical care database."
  s.description = "Open-source structured datasets tracking species-specific watering intervals, light requirements, and soil algorithms."
  s.authors     = ["The Plant Matrix"]
  s.email       = 'contact@theplantmatrix.com'
  s.homepage    = 'https://theplantmatrix.com'
  s.license     = 'MIT'

  s.metadata['homepage_uri']    = 'https://theplantmatrix.com'
  s.metadata['source_code_uri'] = 'https://github.com'
  s.metadata['bug_tracker_uri'] = 'https://theplantmatrix.com'

  s.files       = ["index.html", "README.md"] rescue []
  s.require_paths = ["lib"]
end
